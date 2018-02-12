package gdt

import (
	"net/http"
	"net/url"
	. "quantum/defs/report"
	. "quantum/defs/report/ad/gdt"
	"quantum/util"
	"strconv"
)

func callback_handler(ch chan url.Values, query, config chan Token) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		defer r.Body.Close()
		queryForm, err := url.ParseQuery(r.URL.RawQuery)
		if err != nil {
			util.Log("[Error] Parsing URL parameters ", err)
			return
		}
		//util.Log( "Request Path:", r.URL.Path)
		v, ok := queryForm["authorization_code"]
		if ok {
			ch <- queryForm
			w.Write([]byte("OK"))
			return
		}
		v, ok = queryForm["query"]
		if ok {
			k, ok := queryForm["type"]
			if ok {
				i, _ := strconv.Atoi(k[0])
				j, _ := strconv.Atoi(v[0])
				data := Token{TokenType: i, AccountID: j, Data: ""}
				query <- data
				x := <-query
				w.Write([]byte(x.Data))
				return
			}
			w.Write([]byte(""))
			return
		}
		v, ok = queryForm["config"]
		if ok {
			k, ok := queryForm["type"]
			if ok {
				d, ok := queryForm["data"]
				if ok {
					i, _ := strconv.Atoi(k[0])
					j, _ := strconv.Atoi(v[0])
					data := Token{TokenType: i, AccountID: j, Data: d[0]}
					config <- data
				}
			}
			w.Write([]byte(""))
			return
		}
		w.Write([]byte(""))
	}
}

func set_authorization_code(codes map[int][]string, expired map[int][]int64, last, stat map[int]int64, x url.Values) {
	k, err := strconv.Atoi(x["state"][0])
	if err != nil {
		util.Log("account id not corrected:", x["state"][0])
		return
	}
	v := x["authorization_code"][0]
	_, ok := last[k]
	// 渠道账号刚创建
	if !ok {
		stat[k] = STAT_INIT
	} else {
		ts := util.Timestamp(0)
		// 令牌已过期
		if ts > expired[k][TYPE_REFRESH_TOKEN] {
			stat[k] = STAT_EXPIRED
		}
	}
	codes[k] = []string{v, "", ""}
	expired[k] = []int64{util.Timestamp(0) + EXPIRED_CODE, 0, 0}
}

func set_idle_days(expired map[int][]int64, last, stat map[int]int64, ts int64, x Token, query chan Token) {
	data := DATA_EMPTY
	// 未授权，未初始化过
	_, ok := stat[x.AccountID]
	if !ok {
		query <- Token{x.TokenType, x.AccountID, data}
		return
	}
	switch stat[x.AccountID] {
	// 渠道账号刚创建
	case STAT_INIT:
		if ts < expired[x.AccountID][TYPE_CODE] {
			data = LAST_YEAR
			util.Log("Received Query:", x, " Response INIT Days:", LAST_YEAR)
		}
	// 令牌已过期
	case STAT_EXPIRED:
		k := (last[x.AccountID] - ts) / DAY_SECONDS
		if k != 0 {
			data = strconv.FormatInt(k, 10)
			util.Log("Received Query:", x, " Response Expired Days:", data)
		}
	}
	query <- Token{x.TokenType, x.AccountID, data}
}

func get_token_type(token_type int) string {
	switch token_type {
	case TYPE_CODE:
		return "Authentication Code"
	case TYPE_TOKEN:
		return "Token"
	default:
		return "Refresh Token"
	}
}
func response_token(codes map[int][]string, expired map[int][]int64, ts int64, x Token, query chan Token) {
	data := DATA_EMPTY
	// 未授权
	_, ok := expired[x.AccountID]
	if !ok {
		query <- Token{x.TokenType, x.AccountID, data}
		return
	}
	switch {
	// 令牌过期
	case ts > expired[x.AccountID][x.TokenType]:
		util.Log(get_token_type(x.TokenType), "Expired!", "current timestamp", ts,
			"expired timestamp", expired[x.AccountID][x.TokenType])
		query <- Token{x.TokenType, x.AccountID, data}
	// 令牌处于有效期
	default:
		util.Log(get_token_type(x.TokenType), "OK")
		query <- Token{x.TokenType, x.AccountID, codes[x.AccountID][x.TokenType]}
		// 授权码只用一次就过期
		if x.TokenType == TYPE_CODE {
			codes[x.AccountID][TYPE_CODE] = DATA_EMPTY
			expired[x.AccountID][TYPE_CODE] = EXPIRED_NOW
		}
	}
}

func config_expired_time(codes map[int][]string, expired map[int][]int64, last, stat map[int]int64, ts int64, x Token) {
	// 已完成数据补全，设置状态为已授权以及最近一次访问时间
	if x.TokenType == TYPE_TASK_IDLE_DAYS {
		last[x.AccountID] = ts
		stat[x.AccountID] = STAT_AUTH
	}
	// 已获取令牌，设置状态为已授权及令牌过期时间
	_, ok := codes[x.AccountID]
	if ok {
		codes[x.AccountID][x.TokenType] = x.Data
		util.Log(get_token_type(x.TokenType), "set to", x.Data)
		switch x.TokenType {
		// 配置Token过期时间
		case TYPE_TOKEN:
			expired[x.AccountID][x.TokenType] = ts + EXPIRED_TOKEN
		// 配置Refresh Token过期时间
		case TYPE_REFRESH_TOKEN:
			expired[x.AccountID][TYPE_TOKEN] = EXPIRED_NOW
			expired[x.AccountID][x.TokenType] = ts + EXPIRED_REFRESH_TOKEN
			util.Log("Config Refresh Token to be Expired in", util.ConvertSeconds(ts+EXPIRED_TOKEN))
		}
		// 令牌有效，配置最近一次访问时间
		last[x.AccountID] = ts
		stat[x.AccountID] = STAT_AUTH
	}
}

func HandleCallback(readTimeout, writeTimeout int, quit chan int) {
	ch := make(chan url.Values)
	query := make(chan Token)
	config := make(chan Token)
	codes := make(map[int][]string)
	expired := make(map[int][]int64)
	last := make(map[int]int64)
	stat := make(map[int]int64)
	go util.RunHttpServer(callback_handler(ch, query, config), REDIRECT_PORT, readTimeout, writeTimeout, quit)
	for {
		select {
		case x := <-ch:
			util.Log("Received Callback:", x)
			if len(x["state"]) > 0 && len(x["authorization_code"]) > 0 {
				set_authorization_code(codes, expired, last, stat, x)
			}
		case x := <-query:
			ts := util.Timestamp(0)
			// 获取上次任务至今暂停时间，用于拉取缺失数据或过去一年的初始化数据
			if x.TokenType == TYPE_TASK_IDLE_DAYS {
				set_idle_days(expired, last, stat, ts, x, query)
				continue
			}
			response_token(codes, expired, ts, x, query)
		case x := <-config:
			ts := util.Timestamp(0)
			if len(x.Data) > 0 {
				config_expired_time(codes, expired, last, stat, ts, x)
			}
		}
	}
}
