package sem

import (
	. "quantum/defs/report"
	. "quantum/defs/report/sem"
	"quantum/report/sem/cid"
	"quantum/report/sem/hot"
	"quantum/util"
)

func Run(task_id, service_id, read_timeout, write_timeout int, job CronJob, data string, quit chan int) {
	task_done := make(chan int)
	switch job.Service {
	case SEM_HOT:
		go hot.RunService(task_done)
	case SEM_CID:
		go cid.RunService(data, task_done)
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
