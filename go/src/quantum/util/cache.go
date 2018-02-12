package util

import (
	. "quantum/defs/util"
)

func RunCache(task chan Cache, quit chan int) {
	cache := map[string]int{}
	for {
		select {
		case x := <-task:
			switch x.Type {
			case GET_CACHE:
				k, ok := cache[x.Key]
				if !ok {
					x.Result <- CACHE_MISSING
				} else {
					x.Result <- k
				}
			case SET_CACHE:
				cache[x.Key] = x.Value
			case DEL_CACHE:
				cache = make(map[string]int)
			}
		case <-quit:
			return
		}
	}
}
