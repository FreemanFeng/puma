package sdk

import (
	"time"
)

type TimeoutControl struct {
	Begin    time.Time
	Duration int64
	Done     chan int
}
