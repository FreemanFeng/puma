package cid

import (
	"fmt"
	"net/url"
	. "quantum/defs/report"
	. "quantum/defs/report/sem/cid"
	. "quantum/defs/util"
	"quantum/util"
	"strconv"
	"time"
	"unicode/utf8"
)

func build_params(data string) (url.Values, map[string]string) {
	params := util.ParseParams(data)
	raw := map[string]string{}
	util.FillMissed(params, PARAM_BID, DEFAULT_BID)
	util.FillMissed(params, PARAM_PFID, DEFAULT_PFID)
	util.FillMissed(params, PARAM_PRODUCT, DEFAULT_PRODUCT)
	util.FillRaw(params, PARAM_PUB, DEFAULT_PUB, raw)
	util.FillRaw(params, PARAM_CID, DEFAULT_CID, raw)
	tm := strconv.FormatInt(time.Now().Unix(), 10)
	params[PARAM_TIME] = []string{tm}
	sign := util.SignUrlParams(params, raw, CID_KEY)
	raw[PARAM_SIGN] = sign
	return params, raw
}
func query_cid_status(params url.Values, raw map[string]string) int {
	r := util.BuildUrl(CID_URL, params, raw)
	b := util.HttpRequest(r, "GET", "", map[string]string{})
	msg := &CIDResponse{}
	e := msg.UnmarshalJSON(b)
	if e != nil {
		util.Log("[Error]", e)
		return FAILED_JSON_UNMARSHAL
	}
	fmt.Print(util.Now(), "应答状态:", msg.Status, " 应答消息:")
	for i := 0; i < len(msg.Msg); {
		r, n := utf8.DecodeRuneInString(msg.Msg[i:])
		fmt.Printf("%c", r)
		i += n
	}
	fmt.Println("")
	if len(msg.Data) > 0 {
		util.Log("打包记录:", msg.Data)
	}
	return SUCCESSFUL
}

func RunService(data string, done chan int) {
	params, raw := build_params(data)
	done <- query_cid_status(params, raw)
}
