package util

type Task struct {
	Path, Platform, Service, Request string
	Params                           map[string]string
	Body                             []byte
}

type Cache struct {
	Type   int
	Key    string
	Value  int
	Result chan int
}
