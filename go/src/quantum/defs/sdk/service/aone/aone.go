package aone

type Request struct {
	Author     string `json:"author"`
	AssignTo   string `json:"assignto"`
	Subject    string `json:"subject"`
	TemplateId string `json:"template_id"`
	Stamp      string `json:"stamp"`
	ProjectId  string `json:"project_id"`
	Debug      string `json:"debug"`
	App        string `json:"app"`
	Secret     string `json:"secret"`
}

type Response struct {
	Timestamp string `json:"timestamp"`
	Signature string `json:"signature"`
}
