package util

import (
	"net/url"
	"testing"
)

func TestBuildUrl(t *testing.T) {
	params := url.Values{}
	params["test"] = []string{"HAHA#@%"}
	raw := map[string]string{}
	raw["key"] = "0123456#@%"
	s := BuildUrl("http://non-existing.com", params, raw)
	Log(s)
}

func TestConvertListJsonToMap(t *testing.T) {
	b, p := ConvertListJsonToMap("data")
	Log("prefix:", string(b), "postfix:", string(p))
}

func TestCombineBytes(t *testing.T) {
	b, p := ConvertListJsonToMap("data")
	data := []byte("[ok]")
	r := CombineBytes(b, data, p)
	Log("data:", string(r))
}

func TestConvertJsonData(t *testing.T) {
	b := ConvertListJsonData("data", []byte("[ok]"))
	Log(string(b))
}
