package ad

import (
	. "quantum/defs/report"
	. "quantum/defs/report/ad"
	"quantum/report/ad/gdt"
	"quantum/util"
)

func Run(taskId, serviceId, readTimeout, writeTimeout int, job CronJob, data string, quit chan int) {
	task_done := make(chan int)
	switch job.Service {
	case AD_GDT:
		go gdt.RunService(taskId, serviceId, readTimeout, writeTimeout, job, data, task_done)
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
