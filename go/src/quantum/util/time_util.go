package util

import (
	. "quantum/defs/util"
	"reflect"
	"strconv"
	"strings"
	"time"
)

func ConvertTime(date time.Time, days int) string {
	ret := date.AddDate(0, 0, days)
	return ret.Format("2006-01-02 15:04:05")
}

func ConvertDate(date time.Time, days int) string {
	ret := date.AddDate(0, 0, days)
	return ret.Format("2006-01-02")
}

func GetTime(days int) string {
	now := time.Now().Local()
	return ConvertTime(now, days)
}

func GetDate(days int) string {
	now := time.Now().Local()
	return ConvertDate(now, days)
}

func GetHour() int { //获取当前服务器的小时
	unixTimeStamp := time.Now().Unix()
	timeStamp := time.Unix(unixTimeStamp, 0)
	hr, _, _ := timeStamp.Clock()
	return hr
}

func DateOffset(date string) int {
	s := ConvertMonth(date)
	loc, _ := time.LoadLocation("Local")
	d, _ := time.ParseInLocation("2006-Jan-02", s, loc)
	now := time.Now().Local().Unix()
	return int(d.Unix()-now) / DAY_SECS
}

func DateOffsetString(date string) string {
	offset := DateOffset(date)
	return strconv.Itoa(offset)
}

func ConvertMonth(date string) string {
	s := strings.Split(date, "-")
	m := map[string]string{"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May",
		"06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep",
		"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May",
		"6": "Jun", "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
	d := s[1]
	h := []string{s[0], m[d], s[2]}
	return strings.Join(h, "-")
}

func ConvertSeconds(seconds int64) string {
	t := time.Unix(seconds, 0)
	return ConvertTime(t, 0)
}

func GetYesterday(date string) string {
	s := ConvertMonth(date)
	loc, _ := time.LoadLocation("Local")
	d, _ := time.ParseInLocation("2006-Jan-02", s, loc)
	return ConvertDate(d, -1)
}

func GetLastWeek(date string) string {
	s := ConvertMonth(date)
	loc, _ := time.LoadLocation("Local")
	d, _ := time.ParseInLocation("2006-Jan-02", s, loc)
	return ConvertDate(d, -7)
}

func GetCustomDays(date string, cs int) string {
	s := ConvertMonth(date)
	loc, _ := time.LoadLocation("Local")
	d, _ := time.ParseInLocation("2006-Jan-02", s, loc)
	return ConvertDate(d, cs)
}

func GetLastMonth(date string) string {
	s := ConvertMonth(date)
	loc, _ := time.LoadLocation("Local")
	d, _ := time.ParseInLocation("2006-Jan-02", s, loc)
	return ConvertDate(d, -30)
}

func Timestamp(days int) int64 {
	now := time.Now().Local()
	ts := now.AddDate(0, 0, days)
	return ts.Unix()
}

func Millisecond() int64 {
	return time.Now().UnixNano() / int64(time.Millisecond)
}

func GetTimestamp(days int) string {
	ts := Timestamp(days)
	return strconv.FormatInt(ts, 10)
}

func GetMillisecond() string {
	ts := Millisecond()
	return strconv.FormatInt(ts, 10)
}

func Now() string {
	return time.Now().Format(time.RFC850)
}

func InitTimeoutTrigger(duration int, timeout chan bool) {
	if duration == 0 {
		return
	}
	go func() {
		time.Sleep(time.Duration(duration) * time.Second)
		timeout <- true
	}()
}

func WaitStart(cron_type, start_time int) {
	wait := 0
	now := 0
	timeout := make(chan bool, 1)
	for now != start_time {
		switch cron_type {
		case CRON_TYPE_EVERY_DAYS:
			wait = HOUR_SECS
			now = time.Now().Hour()
		case CRON_TYPE_EVERY_HOURS:
			wait = MIN_SECS
			now = time.Now().Minute()
		case CRON_TYPE_EVERY_MINS:
			now = time.Now().Second()
			wait = ONE_SEC
		default:
			return
		}
		if now == start_time {
			return
		}
		InitTimeoutTrigger(wait, timeout)
		<-timeout
	}
}

func Schedule(cron_type, start_time, interval int, quit chan int, jobFun interface{}, params ...interface{}) {
	secs := 0
	WaitStart(cron_type, start_time)
	f := reflect.ValueOf(jobFun)
	if len(params) != f.Type().NumIn() {
		Log("The number of param is not adapted.")
		quit <- FAILED_FUNC_PARAMS_NOT_ENOUGH
		return
	}
	in := make([]reflect.Value, len(params))
	for k, param := range params {
		in[k] = reflect.ValueOf(param)
	}
	switch cron_type {
	case NO_CRON_JOB:
		f.Call(in)
		quit <- SUCCESSFUL
		return
	case CRON_TYPE_EVERY_DAYS:
		secs = interval * DAY_SECS
	case CRON_TYPE_EVERY_HOURS:
		secs = interval * HOUR_SECS
	case CRON_TYPE_EVERY_MINS:
		secs = interval * MIN_SECS
	case CRON_TYPE_EVERY_SECS:
		secs = interval
	case KEEP_ALIVE:
		secs = YEAR_SECS
	}
	go f.Call(in)
	timeout := make(chan bool, 1)
	InitTimeoutTrigger(secs, timeout)
	for {
		select {
		case <-timeout:
			go f.Call(in)
			InitTimeoutTrigger(secs, timeout)
		}
	}
}
