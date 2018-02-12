package dingding

const (
	TESTING_API = "http://yftest.ucweb.local:9999"
	ONLINE_API  = "https://dd.uc.cn"
)

const (
	PATH_MSG_SEND   = "/msg/send"
	PATH_GROUP_SEND = "/msg/group/send"
	PATH_CHAT_SEND  = "/msg/chat/send"
)

const (
	DEFAULT_MESSAGE = "Hello World!"
	DEFAULT_EMAIL   = "haixiang.fhx@alibaba-inc.com"

	// UC自动化测试
	DEFAULT_CLIENT_ID = 26
	DEFAULT_SECRET    = "fbaa43dbee097b32d163d0bf746afe42"

	// 测试环境
	TESTING_CLIENT_ID = 1
	TESTING_SECRET    = "5a0d027c5483b388e22fbb455616da5e"

	DEFAULT_MOBILE = "12345678900"
	DEFAULT_TYPE   = "text"
)

const (
	PARAM_CLIENT_ID = "clientId"
	PARAM_SECRET    = "secret"
	PARAM_SIGNATURE = "signature"
	PARAM_NONCE     = "nonce"
	PARAM_MESSAGE   = "message"
	PARAM_TYPE      = "type"
	// 公告消息
	PARAM_MSG_MOBILES = "mobiles"
	PARAM_MSG_EMAILS  = "emails"
	// 群组消息
	PARAM_GROUP_ID        = "groupId"
	PARAM_GROUP_ATMOBILES = "atMobiles"
	PARAM_GROUP_ATEMAILS  = "atEmails"
	PARAM_GROUP_ISATALL   = "isAtAll"
	// 点到点消息
	PARAM_CHAT_TITLE = "title"
	PARAM_CHAT_OWNER = "owner"
)

const (
	TYPE_MSG_SEND       = 0
	TYPE_MSG_GROUP_SEND = 1
)
