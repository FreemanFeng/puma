package sdk

import (
	. "quantum/defs/sdk"
	. "quantum/defs/util"
	"quantum/sdk/service/aone"
	"quantum/sdk/service/dingding"
	"quantum/sdk/service/ucstart"
	"quantum/util"
)

func dispatch(task Task, ch chan []byte, cache chan Cache) {
	done := make(chan int)
	defer close(done)
	switch task.Service {
	case DING_DING:
		go dingding.RunService(task, ch, cache, done)
	case AONE:
		go aone.RunService(task, ch, cache, done)
	case UCSTART:
		go ucstart.RunService(task, ch, cache, done)
	default:
		ch <- []byte("Incorrect Request!")
		return
	}
	for {
		select {
		case <-done:
			return
		}
	}
}

func Run(port, readTimeout, writeTimeout int, quit chan int) {
	ch := make(chan Task)
	data_ch := make(chan []byte)
	m := map[string]int{}
	cacheList := []chan Cache{}
	go util.RunHttpServer(util.TaskHandler(ch, data_ch), port, readTimeout, writeTimeout, quit)
	for {
		select {
		case x := <-ch:
			_, ok := m[x.Service]
			if !ok {
				index := len(cacheList)
				m[x.Service] = index
				cacheList = append(cacheList, make(chan Cache))
				go util.RunCache(cacheList[index], quit)
			}
			index := m[x.Service]
			go dispatch(x, data_ch, cacheList[index])
		}
	}
}
