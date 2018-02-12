package util

import (
	"io/ioutil"
	"net/http"
	"net/url"
	. "quantum/defs/util"
	"strings"
)

func TaskHandler(ch chan Task, resp chan []byte) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		defer r.Body.Close()
		task := Task{}
		params, err := url.ParseQuery(r.URL.RawQuery)
		if err != nil {
			Log("[Error] Parsing URL parameters ", err)
			return
		}
		// 获取请求参数
		task.Params = map[string]string{}
		for k, v := range params {
			task.Params[k] = v[0]
		}
		// 获取请求PATH
		task.Path = r.URL.Path
		Log("Request Path:", task.Path)
		paths := strings.Split(task.Path, "/")
		n := len(paths)
		if n < MIN_ROUTES {
			w.Write([]byte("Request Incorrect!"))
			return
		}
		task.Platform = paths[PLATFORM_POS]
		task.Service = paths[SERVICE_POS]
		task.Request = paths[n-1]
		Log("Platform:", task.Platform, " Service:", task.Service, " Request:", task.Request)

		// 提取请求内容
		task.Body, err = ioutil.ReadAll(r.Body)
		if err != nil {
			Log("[Error] Failed in reading request body", err)
			w.Write([]byte(""))
			return
		}

		ch <- task
		data := <-resp
		w.Write(data)
		return
	}
}
