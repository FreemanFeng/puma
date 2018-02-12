package util

import (
	"crypto/tls"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"
)

func RunHttpServer(handler http.HandlerFunc, httpPort, readTimeout, writeTimeout int, quit chan int) {
	Log("Running Http Server on port", httpPort)
	a := []string{":", strconv.Itoa(httpPort)}
	h := strings.Join(a, "")
	s := &http.Server{
		Addr:           h,
		Handler:        handler,
		ReadTimeout:    time.Duration(readTimeout) * time.Second,
		WriteTimeout:   time.Duration(writeTimeout) * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	// disable HTTP/2
	s.TLSNextProto = map[string]func(*http.Server, *tls.Conn, http.Handler){}
	go func() {
		log.Fatal(s.ListenAndServe())
	}()

	select {
	case <-quit:
		Log("Stop Http Server and Quit")
		return
	}
}
func InitRoutes(params ...string) map[string]int {
	r := map[string]int{}
	for _, v := range params {
		r[v] = 1
	}
	return r
}
