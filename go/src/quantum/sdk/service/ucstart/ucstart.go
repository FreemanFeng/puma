package ucstart

import (
	. "quantum/defs/sdk/service/ucstart"
	. "quantum/defs/util"
	"quantum/util"
)

func build_headers() map[string]string {
	headers := map[string]string{}
	headers["Content-Type"] = "application/x-www-form-urlencoded"
	headers["Accept"] = "text/plain"
	return headers
}

func dispatch(task Task, ch chan []byte, cache chan Cache, done chan int) {
	switch task.Request {
	case REQUEST_TEST_SYNC:
		sync_test(task, ch, cache, done)
	case REQUEST_INIT:
		init_client(task, ch, cache, done)
	case REQUEST_GET_ADM:
		mock_adm(task, ch, cache, done)
	case REQUEST_GET_CMS:
		mock_cms(task, ch, cache, done)
	case REQUEST_LOG:
		process_log(task, ch, cache, done)
	}
}

func RunService(task Task, ch chan []byte, cache chan Cache, done chan int) {
	r := util.InitRoutes(REQUEST_TEST_SYNC, REQUEST_INIT, REQUEST_GET_CMS, REQUEST_GET_ADM, REQUEST_LOG)
	_, ok := r[task.Request]
	if !ok {
		ch <- []byte("Incorrect Request!")
		done <- FAILED
	}
	dispatch(task, ch, cache, done)
}
