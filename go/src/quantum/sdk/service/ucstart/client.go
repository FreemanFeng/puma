package ucstart

import (
	. "quantum/defs/sdk/service/ucstart"
	. "quantum/defs/util"
	"quantum/util"
)

func set_cache(key string, cache chan Cache, status int) {
	cache <- Cache{Type: SET_CACHE, Key: key, Value: status}
}

func init_client(task Task, ch chan []byte, cache chan Cache, done chan int) {
	id, ok := task.Params[PARAM_ID]
	if !ok {
		ch <- []byte("Request Param[id] is missing!")
		done <- FAILED
	}
	result := make(chan int)
	cache <- Cache{Type: GET_CACHE, Key: id, Result: result}
	x := <-result
	switch x {
	case CACHE_EXPIRED:
		util.Log("ID ", id, "expired!")
		ch <- []byte("ID expired!")
		done <- SUCCESSFUL
	case CACHE_EXISTS:
		util.Log("ID ", id, "exists!")
		set_cache(id, cache, CACHE_EXPIRED)
		ch <- []byte("ID exists!")
		done <- SUCCESSFUL
	case CACHE_MISSING:
		set_cache(id, cache, CACHE_EXISTS)
		util.Log("ID ", id, " is new!")
		ch <- []byte("ID is new!")
		done <- SUCCESSFUL
	}
}

func process_log(task Task, ch chan []byte, cache chan Cache, done chan int) {
}
