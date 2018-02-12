package gdt

type PageInfoData struct {
	Page      int `json:"page"`
	PageSize  int `json:"page_size"`
	TotalNum  int `json:"total_number"`
	TotalPage int `json:"total_page"`
}

type CampaignsGetDataList struct {
	CampaignID       int64  `json:"campaign_id"`
	CampaignName     string `json:"campaign_name"`
	ConfiguredStatus string `json:"configured_status"`
	CampaignType     string `json:"campaign_type"`
	ProductType      string `json:"product_type"`
	DailyBudget      int64  `json:"daily_budget"`
	BudgetReachDate  int64  `json:"budget_reach_date"`
	CreatedTime      int64  `json:"created_time"`
	LastModifiedTime int64  `json:"last_modified_time"`
}

type CampaignsGetData struct {
	List     []CampaignsGetDataList `json:"list"`
	PageInfo PageInfoData           `json:"page_info"`
}

type CampaignsGetResponse struct {
	Code    int64            `json:"code"`
	Message string           `json:"message"`
	Data    CampaignsGetData `json:"data"`
}

type KeywordsType struct {
	Words []string `json:"words"`
}

type GeoLocationType struct {
	LocationTypes     []string `json:"location_types"`
	Regions           []int64  `json:"regions"`
	BusinessDistricts []int64  `json:"business_districts"`
}

type TargetingType struct {
	Age                       []string        `json:"age"`                         //年龄定向
	Gender                    []string        `json:"gender"`                      //性别定向
	Education                 []string        `json:"education"`                   //用户学历
	RelationshipStatus        []string        `json:"relationship_status"`         //婚恋状态
	LivingStatus              []string        `json:"living_status"`               //生活状态
	BusinessInterest          []int64         `json:"business_interest"`           //商业兴趣定向
	Keyword                   KeywordsType    `json:"keyword"`                     //关键词定向
	GeoLocation               GeoLocationType `json:"geo_location"`                //地理位置定向
	UserOS                    []string        `json:"user_os"`                     //操作系统定向
	NewDevice                 []string        `json:"new_device"`                  //新设备
	DevicePrice               []string        `json:"device_price"`                //设备价格
	NetworkType               []string        `json:"network_type"`                //联网方式定向
	NetworkOperator           []string        `json:"network_operator"`            //移动运营商定向
	DressingIndex             []string        `json:"dressing_index"`              //穿衣指数
	UVIndex                   []string        `json:"uv_index"`                    //紫外线指数
	MakeupIndex               []string        `json:"makeup_index"`                //化妆指数
	Climate                   []string        `json:"climate"`                     //气象
	Temperature               []string        `json:"temperature"`                 //温度
	AppInstallStatus          []string        `json:"app_install_status"`          //应用用户
	AppBehavior               []string        `json:"app_behavior"`                //app 行为定向
	ShoppingCapability        []string        `json:"shopping_capability"`         //消费能力
	PlayerConsupt             []string        `json:"player_consupt"`              //游戏用户消费能力
	PayingUserType            []string        `json:"paying_user_type"`            //付费用户
	ResidentialCommunityPrice []string        `json:"residential_community_price"` //居民社区价格
	CustomAudiences           []string        `json:"custom_audiences"`            //客户人群
	ExcludedCustomAudiences   []string        `json:"excluded_custom_audiences"`   //排除客户人群
}

type AdgroupsGetDataList struct {
	CampaignID               int64         `json:"campaign_id"`
	AdgroupID                int64         `json:"adgroup_id"`
	AdgroupName              string        `json:"adgroup_name"`
	SiteSet                  []string      `json:"site_set"`
	OptimizationGoal         string        `json:"optimization_goal"`
	BillingEvent             string        `json:"billing_event"`
	BidAmount                int64         `json:"bid_amount"`
	DailyBudget              int64         `json:"daily_budget"`
	ProductType              string        `json:"product_type"`
	ProductRefsID            string        `json:"product_refs_id"`
	SubordinateProductRefsID string        `json:"subordinate_product_refs_id"`
	TargetingID              int64         `json:"targeting_id"`
	Targeting                TargetingType `json:"targeting"`
	BeginDate                string        `json:"begin_date"`
	EndDate                  string        `json:"end_date"`
	TimeSeries               string        `json:"time_series"`
	ConfiguredStatus         string        `json:"configured_status"`
	SystemStatus             string        `json:"system_status"`
	RejectMessage            string        `json:"reject_message"`
	CustomizedCategory       string        `json:"customized_category"`
	CreatedTime              int64         `json:"created_time"`
	LastModifiedTime         int64         `json:"last_modified_time"`
}

type AdgroupsGetData struct {
	List     []AdgroupsGetDataList `json:"list"`
	PageInfo PageInfoData          `json:"page_info"`
}

type AdgroupsGetResponse struct {
	Code    int64           `json:"code"`
	Message string          `json:"message"`
	Data    AdgroupsGetData `json:"data"`
}

type CorporateType struct {
	CorporateName string `json:"corporate_name"`
	CorporateImg  string `json:"corporate_img"`
}

type ElementStoryItemType struct {
	Image       string `json:"image"`
	Image2      string `json:"image2"`
	Description string `json:"description"`
	Url         string `json:"url"`
	Title       string `json:"title"`
}

type VideoPopupButtonType struct {
	VideoPopupButtonText string `json:"video_popup_button_text"`
	VideoPopupButtonUrl  string `json:"video_popup_button_url"`
}

type AdcreativeElementsType struct {
	Image               string                 `json:"image"`
	Image2              string                 `json:"image2"`
	Image3              string                 `json:"image3"`
	Title               string                 `json:"title"`
	Description         string                 `json:"description"`
	Corporate           CorporateType          `json:"corporate"`
	DeepLink            string                 `json:"deep_link"`
	Phone               string                 `json:"phone"`
	Video               string                 `json:"video"`
	Caption             string                 `json:"caption"`
	ImageList           []string               `json:"image_list"`
	ElementStory        []ElementStoryItemType `json:"element_story"`
	MultiShareOptimized string                 `json:"multi_share_optimized"`
	Url                 string                 `json:"url"`
	ButtonText          string                 `json:"button_text"`
	VideoPopupUrl       string                 `json:"video_popup_url"`
	VideoPopupButton    VideoPopupButtonType   `json:"video_popup_button"`
	Image2Url           string                 `json:"image2_url"`
	Image3Url           string                 `json:"image3_url"`
	ImageListUrl        []string               `json:"image_list_url"`
	VideoUrl            string                 `json:"video_url"`
}

type AdcreativeGetDataList struct {
	CampaignID           int64                  `json:"campaign_id"`
	AdcreativeID         int64                  `json:"adcreative_id"`
	AdcreativeName       string                 `json:"adcreative_name"`
	AdcreativeTemplateID int64                  `json:"adcreative_template_id"`
	AdcreativeElements   AdcreativeElementsType `json:"adcreative_elements"`
	DestinationUrl       string                 `json:"destination_url"`
	SiteSet              []string               `json:"site_set"`
	ProductType          string                 `json:"product_type"`
	ProductRefsID        string                 `json:"product_refs_id"`
	CreatedTime          int64                  `json:"created_time"`
	LastModifiedTime     int64                  `json:"last_modified_time"`
}

type AdcreativeGetData struct {
	List     []AdcreativeGetDataList `json:"list"`
	PageInfo PageInfoData            `json:"page_info"`
}

type AdcreativeGetResponse struct {
	Code    int64             `json:"code"`
	Message string            `json:"message"`
	Data    AdcreativeGetData `json:"data"`
}

type AdsGetDataList struct {
	CampaignID            int64                 `json:"campaign_id"`
	AdgroupID             int64                 `json:"adgroup_id"`
	AdID                  int64                 `json:"ad_id"`
	AdName                string                `json:"ad_name"`
	Adcreative            AdcreativeGetDataList `json:"adcreative"`
	ConfiguredStatus      string                `json:"configured_status"`
	SystemStatus          string                `json:"system_status"`
	ImpressionTrackingUrl string                `json:"impression_tracking_url"`
	ClickTrackingUrl      string                `json:"click_tracking_url"`
	RejectMessage         string                `json:"reject_message"`
	CreatedTime           int64                 `json:"created_time"`
	LastModifiedTime      int64                 `json:"last_modified_time"`
}

type AdsGetData struct {
	List     []AdsGetDataList `json:"list"`
	PageInfo PageInfoData     `json:"page_info"`
}

type AdsGetResponse struct {
	Code    int64      `json:"code"`
	Message string     `json:"message"`
	Data    AdsGetData `json:"data"`
}

type ProductTypeAppleAppStoreType struct {
	AppPropertyPackname          string `json:"app_property_packname"`
	AppPropertyVersion           string `json:"app_property_version"`
	AppPropertyIconUrl           string `json:"app_property_icon_url"`
	AppPropertyIconUrl512        string `json:"app_property_icon_url_512"`
	AppPropertyAverageUserRating string `json:"app_property_average_user_rating"`
	AppPropertyPackageSizeBytes  string `json:"app_property_package_size_bytes"`
	AppPropertyGenres            string `json:"app_property_genres"`
	AppPropertyPkgUrl            string `json:"app_property_pkg_url"`
}

type ProductTypeAppAndroidOpenPlatformType struct {
	AppPropertyPackname          string `json:"app_property_packname"`
	AppPropertyVersion           string `json:"app_property_version"`
	AppPropertyIconUrl           string `json:"app_property_icon_url"`
	AppPropertyAverageUserRating string `json:"app_property_average_user_rating"`
	AppPropertyPackageSizeBytes  string `json:"app_property_package_size_bytes"`
	AppPropertyGenres            string `json:"app_property_genres"`
	AppPropertyPkgUrl            string `json:"app_property_pkg_url"`
}

type ProductTypeUnionAppInfoType struct {
	AppPropertyPackname         string `json:"app_property_packname"`
	AppPropertyVersion          string `json:"app_property_version"`
	AppPropertyIconUrl          string `json:"app_property_icon_url"`
	AppPropertyPackageSizeBytes string `json:"app_property_package_size_bytes"`
	AppPropertyPkgMd5           string `json:"app_property_pkg_md5"`
	AppPropertyPkgUrl           string `json:"app_property_pkg_url"`
}

type ProductInfoType struct {
	ProductTypeAppleAppStore          ProductTypeAppleAppStoreType          `json:"product_type_apple_app_store"`
	ProductTypeAppAndroidOpenPlatform ProductTypeAppAndroidOpenPlatformType `json:"product_type_app_android_open_platform"`
	ProductTypeUnionAppInfo           ProductTypeUnionAppInfoType           `json:"product_type_union_app_info"`
}

type SubordinateProduct struct {
	SubProductRefsID string `json:"sub_product_refs_id"`
	PackageName      string `json:"package_name"`
}
type ProductsGetDataList struct {
	ProductRefsID          string               `json:"product_refs_id"`
	ProductName            string               `json:"product_name"`
	ProductType            string               `json:"product_type"`
	ProductInfo            ProductInfoType      `json:"product_info"`
	SubordinateProductList []SubordinateProduct `json:"subordinate_product_list"`
	CreatedTime            int64                `json:"created_time"`
	LastModifiedTime       int64                `json:"last_modified_time"`
}

type ProductsGetData struct {
	List     []ProductsGetDataList `json:"list"`
	PageInfo PageInfoData          `json:"page_info"`
}

//获取标的物
type ProductsGetResponse struct {
	Code    int64           `json:"code"`
	Message string          `json:"message"`
	Data    ProductsGetData `json:"data"`
}

type TokenData struct {
	AccessToken           string `json:"access_token"`
	RefreshToken          string `json:"refresh_token"`
	AccessTokenExpiresIn  int64  `json:"access_token_expires_in"`
	RefreshTokenExpiresIn int64  `json:"refresh_token_expires_in"`
}

type TokenResponse struct {
	Code    int64     `json:"code"`
	Message string    `json:"message"`
	Data    TokenData `json:"data"`
}

type DailyReportsGetDataList struct {
	Date          string `json:"date"`
	CampaignID    int64  `json:"campaign_id"`
	AdgroupID     int64  `json:"adgroup_id"`
	Impression    int64  `json:"impression"`
	Click         int64  `json:"click"`
	Cost          int64  `json:"cost"`
	Download      int64  `json:"download"`
	Conversion    int64  `json:"conversion"`
	Activation    int64  `json:"activation"`
	LikeOrComment int64  `json:"like_or_comment"`
	ImageClick    int64  `json:"image_click"`
	Follow        int64  `json:"follow"`
	Share         int64  `json:"share"`
}

type DailyReportsGetData struct {
	List     []DailyReportsGetDataList `json:"list"`
	PageInfo PageInfoData              `json:"page_info"`
}

type DailyReportsGetResponse struct {
	Code    int64               `json:"code"`
	Message string              `json:"message"`
	Data    DailyReportsGetData `json:"data"`
}

type HourlyReportsGetDataList struct {
	Hour          int64 `json:"hour"`
	CampaignID    int64 `json:"campaign_id"`
	AdgroupID     int64 `json:"adgroup_id"`
	Impression    int64 `json:"impression"`
	Click         int64 `json:"click"`
	Cost          int64 `json:"cost"`
	Download      int64 `json:"download"`
	Conversion    int64 `json:"conversion"`
	Activation    int64 `json:"activation"`
	LikeOrComment int64 `json:"like_or_comment"`
	ImageClick    int64 `json:"image_click"`
	Follow        int64 `json:"follow"`
	Share         int64 `json:"share"`
}

type HourlyReportsGetData struct {
	List     []HourlyReportsGetDataList `json:"list"`
	PageInfo PageInfoData               `json:"page_info"`
}

type HourlyReportsGetResponse struct {
	Code    int64                `json:"code"`
	Message string               `json:"message"`
	Data    HourlyReportsGetData `json:"data"`
}

type ImageCreateData struct {
	ImageID        string `json:"image_id"`
	ImageWidth     int64  `json:"image_width"`
	ImageHeight    int64  `json:"image_height"`
	ImageFileSize  int64  `json:"image_file_size"`
	ImageType      string `json:"image_type"`
	ImageSignature string `json:"image_signature"`
	OuterImageID   string `json:"outer_image_id"`
}

type ImageCreateResponse struct {
	Code    int64           `json:"code"`
	Message string          `json:"message"`
	Data    ImageCreateData `json:"data"`
}

type ImageCreateByUrlData struct {
	ImageID        string `json:"image_id"`
	ImageWidth     int64  `json:"image_width"`
	ImageHeight    int64  `json:"image_height"`
	ImageFileSize  int64  `json:"image_file_size"`
	ImageType      string `json:"image_type"`
	ImageSignature string `json:"image_signature"`
	OuterImageID   string `json:"outer_image_id"`
}

type ImageCreateByUrlResponse struct {
	Code    int64                `json:"code"`
	Message string               `json:"message"`
	Data    ImageCreateByUrlData `json:"data"`
}

type ImageReadData struct {
	ImageID        string `json:"image_id"`
	ImageWidth     int64  `json:"image_width"`
	ImageHeight    int64  `json:"image_height"`
	ImageFileSize  int64  `json:"image_file_size"`
	ImageType      string `json:"image_type"`
	ImageSignature string `json:"image_signature"`
	PreviewURL     string `json:"preview_url"`
	OuterImageID   string `json:"outer_image_id"`
}

type ImageReadResponse struct {
	Code    int64         `json:"code"`
	Message string        `json:"message"`
	Data    ImageReadData `json:"data"`
}

type ImageSelectDataList struct {
	ImageID        string `json:"image_id"`
	ImageWidth     int64  `json:"image_width"`
	ImageHeight    int64  `json:"image_height"`
	ImageFileSize  int64  `json:"image_file_size"`
	ImageType      string `json:"image_type"`
	ImageSignature string `json:"image_signature"`
	PreviewURL     string `json:"preview_url"`
	OuterImageID   string `json:"outer_image_id"`
}

type ImageSelectData struct {
	List     []ImageSelectDataList `json:"list"`
	PageInfo PageInfoData          `json:"page_info"`
}

type ImageSelectResponse struct {
	Code    int64           `json:"code"`
	Message string          `json:"message"`
	Data    ImageSelectData `json:"data"`
}

type MediaCreateData struct {
	MediaID string `json:"media_id"`
}
type MediaCreateResponse struct {
	Code    int64           `json:"code"`
	Message string          `json:"message"`
	Data    MediaCreateData `json:"data"`
}

type MediaReadData struct {
	MediaDescription string `json:"media_description"`
	MediaWidth       int64  `json:"media_width"`
	MediaHeight      int64  `json:"media_height"`
	VideoFrames      int64  `json:"video_frames"`
	VideoFps         int64  `json:"video_fps"`
	VideoCodec       string `json:"video_codec"`
	VideoBitRate     int64  `json:"video_bit_rate"`
	AudioCodec       string `json:"audio_codec"`
	AudioBitRate     int64  `json:"audio_bit_rate"`
	MediaFileSize    int64  `json:"media_file_size"`
	MediaType        string `json:"media_type"`
	MediaSignature   string `json:"media_signature"`
	SystemStatus     string `json:"system_status"`
	PreviewURL       string `json:"preview_url"`
}

type MediaReadResponse struct {
	Code    int64         `json:"code"`
	Message string        `json:"message"`
	Data    MediaReadData `json:"data"`
}

type MediaSelectDataList struct {
	MediaID          int64  `json:"media_id"`
	MediaDescription string `json:"media_description"`
	MediaWidth       int64  `json:"media_width"`
	MediaHeight      int64  `json:"media_height"`
	VideoFrames      int64  `json:"video_frames"`
	VideoFps         int64  `json:"video_fps"`
	VideoCodec       string `json:"video_codec"`
	VideoBitRate     int64  `json:"video_bit_rate"`
	AudioCodec       string `json:"audio_codec"`
	AudioBitRate     int64  `json:"audio_bit_rate"`
	MediaFileSize    int64  `json:"media_file_size"`
	MediaType        string `json:"media_type"`
	MediaSignature   string `json:"media_signature"`
	SystemStatus     string `json:"system_status"`
	PreviewURL       string `json:"preview_url"`
}

type MediaSelectData struct {
	List     []MediaSelectDataList `json:"list"`
	PageInfo PageInfoData          `json:"page_info"`
}

type MediaSelectResponse struct {
	Code    int64           `json:"code"`
	Message string          `json:"message"`
	Data    MediaSelectData `json:"data"`
}

type RequestData struct {
	ServiceID int64  `json:"service_id"`
	Params    string `json:"params"`
}
