package report

import (
	"io/ioutil"
	"os"
	. "quantum/defs/report"
	. "quantum/defs/util"
	"quantum/report/ad"
	"quantum/report/sem"
	"quantum/report/store"
	"quantum/util"
)

func parse_config(file string) TaskConfig {
	body, err := ioutil.ReadFile(file)
	if err != nil {
		util.Log("Error in Reading Task Config File")
		os.Exit(1)
	}
	msg := TaskConfig{}
	err = msg.UnmarshalJSON(body)
	if err != nil {
		util.Log("Error in Parsing Task Config")
		os.Exit(1)
	}
	return msg
}

func run_task(jobId, taskId, taskTimeout, readTimeout, writeTimeout, serviceId int, job CronJob, params string, quit chan int) {
	task_done := make(chan int)
	switch job.Platform {
	case PLATFORM_SEM:
		go sem.Run(taskId, serviceId, readTimeout, writeTimeout, job, params, task_done)
	case PLATFORM_AD:
		go ad.Run(taskId, serviceId, readTimeout, writeTimeout, job, params, task_done)
	case PLATFORM_STORE:
		go store.Run(taskId, serviceId, readTimeout, writeTimeout, job, params, task_done)
	}

	timeout := make(chan bool, 1)
	util.InitTimeoutTrigger(taskTimeout, timeout)
	select {
	case x := <-task_done:
		switch x {
		case SUCCESSFUL:
			util.Log("Job", jobId, "Task", taskId, job.Platform,
				job.Service, job.Account, params, "Done Successful!")
		default:
			util.Log("Job", jobId, "Task", taskId, job.Platform,
				job.Service, job.Account, params, "Failed!")
		}
		quit <- x
	case <-timeout:
		util.Log("Timeout for receiving callback request")
		quit <- FAILED_TIMEOUT
	}
}

func run_client(job_id int, job CronJob, taskTimeout, readTimeout, writeTimeout int, quit chan int) {
	task_done := make(chan int)
	for i, task := range job.Data {
		go run_task(job_id, i, taskTimeout, readTimeout, writeTimeout, task.ServiceID, job, task.Params, task_done)
	}
	for {
		select {
		case <-task_done:
			return
		}
	}
}

func run_periodically(jobId, interval, cronType, taskTimeout, readTimeout, writeTimeout, start_time int, job CronJob, quit chan int) {
	done := make(chan int)
	secs := 0
	util.WaitStart(cronType, start_time)
	switch cronType {
	case NO_CRON_JOB:
		run_client(jobId, job, taskTimeout, readTimeout, writeTimeout, done)
		quit <- SUCCESSFUL
		return
	case CRON_TYPE_EVERY_DAYS:
		secs = interval * DAY_SECS
	case CRON_TYPE_EVERY_HOURS:
		secs = interval * HOUR_SECS
	case CRON_TYPE_EVERY_MINS:
		secs = interval * MIN_SECS
	case CRON_TYPE_EVERY_SECS:
		secs = interval
	}
	timeout := make(chan bool, 1)
	util.InitTimeoutTrigger(secs, timeout)
	for {
		select {
		case <-timeout:
			go run_client(jobId, job, taskTimeout, readTimeout, writeTimeout, done)
			util.InitTimeoutTrigger(secs, timeout)
		}
	}
}

func Run(config string, taskTimeout, readTimeout, writeTimeout int, quit chan int) {
	if len(config) == 0 {
		return
	}
	msg := parse_config(config)
	total := 0
	for i, job := range msg.Jobs {
		//同一个调度类型（如按天，按小时或按分钟），可以有多次调度
		for _, start := range job.Start {
			done := make(chan int)
			go util.Schedule(job.CronType, start, job.Interval, quit, run_client, i, job, taskTimeout, readTimeout, writeTimeout, done)
			total++
		}
	}
	for {
		select {
		case <-quit:
			total--
			if total <= 0 {
				return
			}
		}
	}
}
