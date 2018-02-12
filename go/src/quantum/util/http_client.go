package util

import (
	"bytes"
	"crypto/tls"
	"io/ioutil"
	"net/http"
	"net/url"
	. "quantum/defs/util"
	"sort"
	"strings"
)

func HttpRequest(url, method, body string, headers map[string]string) []byte {
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	client := &http.Client{Transport: tr}

	req, err := http.NewRequest(method, url, strings.NewReader(body))
	if err != nil {
		Log(err)
		return []byte("")
	}

	for k, v := range headers {
		req.Header.Add(k, v)
	}

	resp, err := client.Do(req)
	if err != nil {
		Log(err)
		return []byte("")
	}

	defer resp.Body.Close()
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		Log(err)
		return []byte("")
	}
	Log(method, " ", url, " [", resp.Status, "]")
	//fmt.Println(string(b))
	return b
}

func CombineParamsSorted(h, keys, data []string, sep string) string {
	for i, k := range keys {
		t := []string{k, data[i]}
		h = append(h, strings.Join(t, "="))
	}
	return strings.Join(h, sep)
}

func CombineListParamsSorted(h, keys, data []string) string {
	return CombineParamsSorted(h, keys, data, "")
}

func CombineUrlParamsSorted(h, keys, data []string) string {
	return CombineParamsSorted(h, keys, data, "&")
}

func CombineUrlParams(h []string, params map[string]string) string {
	for k, v := range params {
		t := []string{k, v}
		h = append(h, strings.Join(t, "="))
	}
	return strings.Join(h, "&")
}

func BuildUrl(base_url string, enc_params url.Values, raw_params map[string]string) string {
	s := []string{base_url, enc_params.Encode()}
	r := strings.Join(s, "?")
	t := CombineUrlParams([]string{r}, raw_params)
	Log("Built URL:", t)
	return t
}

func SortMapString(params map[string]string) ([]string, []string) {
	keys := make([]string, len(params))
	data := make([]string, len(params))
	index := 0
	for k := range params {
		keys[index] = k
		index++
	}
	sort.Strings(keys)
	for i, k := range keys {
		data[i] = params[k]
	}
	return keys, data
}

func CombineParams(enc_params url.Values, raw_params map[string]string) map[string]string {
	params := map[string]string{}
	for k, v := range raw_params {
		params[k] = v
	}
	for k, v := range enc_params {
		params[k] = v[0]
	}
	return params
}

func SortUrlParams(enc_params url.Values, raw_params map[string]string) ([]string, []string) {
	params := CombineParams(enc_params, raw_params)
	return SortMapString(params)
}

func ConvertListJsonToMap(key string) ([]byte, []byte) {
	s := []string{"{", STR_DOUBLE_QUOTES, key, STR_DOUBLE_QUOTES, ":"}
	h := strings.Join(s, "")
	b := []byte(h)
	p := []byte("}")
	return b, p
}

func CombineBytes(data ...[]byte) []byte {
	b := append([][]byte{}, data...)
	return bytes.Join(b, []byte{})
}

func ConvertListJsonData(key string, body []byte) []byte {
	b, p := ConvertListJsonToMap(key)
	return CombineBytes(b, body, p)
}
