package store

import (
	. "quantum/defs/report"
	. "quantum/defs/report/store"
	"quantum/report/store/pp"
	"quantum/report/store/wdj"
	"quantum/util"
)

func Run(task_id, service_id, read_timeout, write_timeout int, job CronJob, data string, quit chan int) {
	task_done := make(chan int)
	switch job.Service {
	case STORE_PP:
		go pp.RunService(task_id, service_id, job.Account, data, task_done)
	case STORE_WDJ:
		go wdj.RunService(task_id, service_id, job.Account, data, task_done)
	default:
		util.Log("[FATAL ERROR]Unknown Service ID")
	}
	for {
		select {
		case x := <-task_done:
			quit <- x
			return
		}
	}
}
