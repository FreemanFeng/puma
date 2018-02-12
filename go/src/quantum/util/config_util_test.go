package util

import (
	"testing"
)

func TestParseConfig(t *testing.T) {
	s := "a=b&c=d&e=f|h=i&j=k"
	p, c := ParseConfig(s)
	Log("req params:", p, "ctl params:", c)
}
