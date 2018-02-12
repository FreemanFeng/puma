package util

import (
	"testing"
)

func TestMD5Sum(t *testing.T) {
	b := MD5Sum("http://non-existing.com", "00000000000", "11111111111")
	Log("MD5 output:", string(b[:]))
}
