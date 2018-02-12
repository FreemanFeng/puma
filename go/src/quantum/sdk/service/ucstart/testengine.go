package ucstart

import (
	. "quantum/defs/util"
	"quantum/util"
)

func sync_test(task Task, ch chan []byte, cache chan Cache, done chan int) {
	for k, v := range task.Params {
		util.Log("k:", k, " v:", v)
	}
}

func run_test_engine(task Task, ch chan []byte, done chan int) {
}
