package ucstart

type Request struct {
	ClientId int    `json:"clientId"`
	Secret   string `json:"secret"`
	Message  string `json:"message"`
	Type     string `json:"type"`
	// 公告消息
	Emails  []string `json:"emails"`
	Mobiles []string `json:"mobiles"`
	// 群组消息
	GroupId   string   `json:"groupId"`
	AtMobiles []string `json:"atMobiles"`
	AtEmails  []string `json:"atEmails"`
	IsAtAll   string   `json:"isAtAll"`
	// 点到点消息
	Title string `json:"title"`
	Owner string `json:"owner"`
}

type Body struct {
	ClientId  int    `json:"clientId"`
	Signature string `json:"signature"`
	Nonce     string `json:"nonce"`
	Message   string `json:"message"`
	Type      string `json:"type"`
	// 公告消息
	Mobiles string `json:"mobiles"`
	Emails  string `json:"emails"`
	// 群组消息
	GroupId   string `json:"groupId"`
	AtMobiles string `json:"atMobiles"`
	AtEmails  string `json:"atEmails"`
	IsAtAll   string `json:"isAtAll"`
}

type ResponseData struct {
	Uuid           string `json:"uuid"`
	InvalidMobiles string `json:"invalidMobiles"`
	InvalidEmails  string `json:"invalidEmails"`
}

type Response struct {
	Code    int          `json:"code"`
	Message string       `json:"message"`
	Data    ResponseData `json:"data"`
}
