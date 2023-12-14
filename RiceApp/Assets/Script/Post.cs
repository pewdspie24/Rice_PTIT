using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Post
{
    public string file { get; set; }
}

public class Demo
{
    public string Title { get; set; }
    public string Body { get; set; }
    public int UserId { get; set; }
}
[Serializable]
public class ReturnedClass
{
    public string type { get; set; }
    public int _intClass { get; set; }
    public float confidence { get; set; }
    public int errorStat { get; set; }
    public String desc { get; set; }
    public ReturnedClass()
    {
        type = "UNKNOWN";
        _intClass = 0;
        confidence = 0.0f;
        errorStat = 1;
    }
    public ReturnedClass(int _err)
    {
        type = "UNKNOWN";
        _intClass = 0;
        confidence = 0.0f;
        errorStat = _err;
    }
    public ReturnedClass(string _type, float _confidence)
    {
        type = _type;
        confidence = _confidence;
        switch (type)
        {
            default:
                _intClass = 0;
                break;
            case "BrownSpot":
                _intClass = 1;
                type = "Bệnh đốm nâu";
                desc = brownSpotDes;
                break;
            case "Healthy":
                _intClass = 2;
                type = "Khỏe mạnh";
                desc = healthyDes;
                break;
            case "Hispa":
                _intClass = 3;
                type = "Bệnh bạc gai";
                desc = hispaDes;
                break;
            case "LeafBlast":
                _intClass = 4;
                type = "Bệnh bạc lá";
                desc = leafBlastDes;
                break;
        }
        errorStat = 1;
    }

    public static String leafBlastDes = "Nguyên nhân: Bệnh bạc lá vi khuẩn lá do vi khuẩn Xanthomonas Oryzae gây ra, bệnh gây hại trong suốt quá trình sinh trưởng phát triển của cây lúa, nhưng biểu hiện rõ và gây hại nặng vào giai đoạn làm đòng - trỗ - chín, nếu không được phòng trừ kịp thời.\n\nTriệu chứng: Bệnh bạc lá xuất hiện ở mép lá, vết bệnh chạy dọc mép lá từ đầu chóp lá chảy xuống; buổi chiều những giọt keo vi khuẩn bạc lá khô đọng lại ở mép lá, có màu vàng, kích thước nhỏ như trứng cá; vào buổi đêm sương, những giọt keo vi khuẩn này tan ra, chảy chạy dài theo mép lá và gió làm xây xát lan sang những lá khác; bệnh nặng khiến cho lá lúa bị cháy, đặc biệt là lá đòng cháy khiến cho lúa bị lép lửng, đen hạt với tỷ lệ cao, làm giảm năng suất nghiêm trọng.\n\nĐặc điểm phát sinh: Trong điều kiện thời tiết nóng ẩm, nắng mưa xen kẻ, ngày nắng đêm mưa, nhiệt độ 26-300C, ẩm độ không khí trên 90%, đặc biệt có mưa to, gió, bão; vi khuẩn xâm nhập và gây hại qua lỗ khí khổng và các vết thương cơ giới trên lá lúa trong điều kiện mưa ẩm thuận lợi cho việc phát triển của vi khuẩn, trên mặt lá bệnh tiết ra những giọt keo vi khuẩn thông qua sự va chạm giữa các lá lúa, truyền bệnh cho các lá khỏe nhờ mưa gió; trên những chân ruộng sâu trũng, màu mỡ, bón phân không cân đối, bón thừa đạm, thiếu kali,  cây lúa xanh tốt, thân mềm yếu, hàm lượng đạm tự do trong cây tích lũy cao thì cây dễ bị nhiễm bệnh nặng; đặc biệt những chân ruộng chua, trũng, gieo cấy, sạ dày, vùng đất hẩu, hàng lúa bị bóng cây che phủ thì bệnh phát triển và gây hại nặng hơn.\n\nBiện pháp phòng trừ:  Để phòng trừ bệnh bạc lá vi khuẩn hiệu quả cần áp dụng biện pháp quản lý dịch hại tổng hợp IPM. Trong đó, việc chọn giống kháng bệnh, chăm sóc cây khỏe đặt lên hàng đầu, cấy thưa 1-2 dảnh/khóm, bón phân cân đối dinh dưỡng NPK, bón nặng đầu nhẹ cuối, bón tập trung sau khi gieo cấy 7-10 ngày, tạo điều kiện cho cây lúa sinh trưởng phát triển khỏe, tăng khả năng chống chịu bệnh ngay từ giai đoạn đầu; áp dụng chế độ tưới nước Nông - Lộ - Phơi hợp lý, tạo cho cây lúa cứng cây, cứng lá vừa tăng khả năng chống đổ cho cây lúa; thường xuyên thăm đồng phát hiện bệnh sớm; khi bệnh xuất hiện cần ngưng ngay việc bón phân đạm, phân bón lá, chất kích thích sinh trưởng (chỉ bón lại khi cây khỏi bệnh); sử dụng thuốc bảo vệ thực vật đặc trị bệnh bạc lá vi khuẩn nằm trong Danh mục thuốc bảo vệ thực vật được phép sử dụng tại Việt Nam có chứa các hoạt chất như:  Copper Hydroxide; Oxolinic acid; Thiodiaxole Zinc; Thiodiazol copper... để phun trừ bệnh.";
    public static String brownSpotDes = "Nguyên nhân: Bệnh đốm nâu có thể do vài loại nấm gây ra, nhưng chủ yếu vẫn là hai loài nấm có tên là Helminthosporium oryzae và nấm Curvularia lunata.\n\nLoài nấm thứ nhất gây ra triệu chứng là ban đầu vết bệnh chỉ nhỏ như đầu mũi kim màu nâu nhạt sau lớn rộng dần ra thành hình bầu dục nhỏ, gần giống như hạt mè, có màu nâu, nâu đậm ở cả hai mặt vết bệnh, xung quanh thường có quầng vàng rất nhỏ. Nếu điều kiện thuận lợi cho bệnh thì vết bệnh lớn hơn, ngược lại nếu thời tiết không thuận lợi cho bệnh thì vết bệnh có kích thước nhỏ hơn (trước đây gọi là bệnh tiêm lửa).\n\nLoài nấm thứ hai gây ra triệu chứng là vết bệnh hình sọc ngắn hoặc không định hình màu nâu tím hoặc nâu xám, cũng có khi là những chấm nhỏ gần tròn màu nâu, nâu tím hoặc nâu xám. Ở trên hạt, vết bệnh là những vết tròn nhỏ gần giống vết bệnh do loại nấm thứ nhất gây ra (trước đây gọi là bệnh đốm nâu hay vết nâu).\n\n Triệu chứng: Vết bệnh trên lá ban đầu là những chấm nhỏ màu nâu nhạt, sau đó phát triển thành các vết bệnh màu nâu đậm hơn. Ở giống lúa kháng nhẹ, đốm bệnh hẹp, ngắn, màu nâu đậm có kích thước từ 2 - 10x1 mm; với những giống nhiễm bệnh, đốm bệnh dài và rộng hơn, có màu nâu nhạt hơn và ở giữa có màu sáng. Tổng thể đốm bệnh thường có màu nâu đỏ, ở mép lá màu nhạt hơn nên ruộng bị nhiễm nặng có màu đỏ rực. Vết bệnh gây hại trên hạt có màu nâu, sau biến màu đen. Nấm bệnh tồn tại trên hạt và là nguồn bệnh cho vụ sau.\n\nĐiều kiện phát sinh bệnh: Do điều kiện phát sinh phát triển của hai loài nấm này rất giống nhau, mặt khác vết bệnh do hai loài nấm này gây ra lại nằm xen kẽ với nhau trên cùng một cây lúa. Vết bệnh do chúng gây ra trên lá tuy có khác nhau ở một số chi tiết, nhưng cũng có những nét tương tự giống nhau. Bệnh đốm nâu phát triển ở vùng đất nghèo chất dinh dưỡng như vùng đất phèn, vùng đất cát bán sơn địa ven chân núi hay ở vùng đất bị ngộ độc hữu cơ, nói chung là những nơi đất có vấn đề làm bộ rễ lúa phát triển kém. Bệnh cũng thường xuất hiện ở những vùng đất quá úng hay khô hạn làm cho cây lúa thiếu nước, khả năng hút dinh dưỡng của bộ rễ gặp nhiều khó khăn khiến cây lúa sinh trưởng kém. Những ruộng bạc màu nghèo dinh dưỡng, những ruộng lúa thiếu phân bón, những giống lúa phàm ăn, nhưng không được cung cấp đủ phân (nhất là phân đạm).... Bệnh phát sinh phát triển thích hợp trong điều kiện nhiệt độ cao, ẩm độ thấp.\n\nCác biện pháp phòng ngừa: Để hạn chế tác hại của bệnh đốm nâu có thể áp dụng kết hợp nhiều biện pháp, trong đó chủ yếu là những biện pháp canh tác, đặc biệt là phân bón và điều tiết nước phù hợp giai đoạn sinh trưởng cây lúa nhằm tạo điều kiện thuân lợi cho cây lúa sinh trưởng, phát triển tốt, tăng sức chống chịu với bệnh từ đó hạn chế tác hại do bệnh gây ra. Sau đây là một số biện pháp chính:\n\n- Cày bừa, xới xáo làm đất kỹ (trừ những chân đất có tầng phèn nằm cạn, dễ bị xì phèn khi làm đất), những ruộng đất bạc màu, đất cát cần bón nhiều phân chuồng để cải tạo và tăng cường chất dinh dưỡng cho đất.\n\n- Không nên gieo sạ quá dày, dễ làm lúa thiếu thức ăn dẫn đến sinh trưởng, phát triển kém, bệnh dễ phát sinh.\n\n- Những ruộng bị nhiễm phèn hoặc dư thừa xác hữu cơ cần tăng cường bón thêm vôi bột, phân lân... để thúc đẩy nhanh quá trình phân hủy chất hữu cơ và nâng cao độ pH cho đất, tạo điều kiện cho cây lúa sinh trưởng và phát triển tốt.\n\n- Phải luôn cung cấp đầy đủ nước cho ruộng lúa, nhất là vào đầu vụ Hè Thu thời tiết khô hạn, nếu thiếu nước làm cho phèn từ tầng đất dưới sẽ xì lên tầng canh tác gây ngộ độc rễ làm cây lúa sinh trưởng kém, tạo điều kiện cho bệnh tấn công.\n\n- Phải bón đầy đủ và cân đối giữa đạm, lân và kali (nhất là với những giống phàm ăn), tuyệt đối không được để cây lúa thiếu đạm, thiếu dinh dưỡng sẽ sinh trưởng phát triển kém.\n\n- Sau khi thu hoạc lúa cần vệ sinh đồng ruộng sạch sẽ, thu dọn sạch tàn dư cây lúa để hạn chế nguồn bệnh ban đầu lan truyền cho vụ sau.\n\n- Không lấy lúa ở những ruộng vụ trước đã bị nhiễm bệnh nặng để làm giống cho vụ sau. Trước khi ngâm ủ phải phơi khô, quạt thật sạch để loại bỏ hết những hạt lép lửng (là những hạt mang nhiều nấm bệnh).\n\n- Do nấm bệnh tồn tại ngay trên vỏ trấu vì thế để diệt trừ một cách triệt để nguồn bệnh ban đầu lây nhiễm cho vụ sau, trước khi ngâm ủ phải xử lý giống bằng nước nóng 540C (3 sôi- 2 lạnh) sau đó vớt ra đãi sạch rồi đem ủ bình thường.\n\nCùng với những biện pháp trên, khi ruộng lúa có biểu hiện bị bệnh có thể sử dụng một trong các loại thuốc có tác dụng phổ rộng như Tilt Super 300EC, AmistarTop 325SC, Viroval 50WP, Hạt vàng 50WP,… để phòng trừ.";
    public static String hispaDes = "Nguyên nhân: xuất phát từ bọ trưởng thành và ấu trùng của loài bọ gai hại lúa có tên khoa học là Dicladispa armigera. Bọ trưởng thành nạo mặt trên của phiến lá để lộ ra lớp biểu bì bên dưới. Chúng đẻ trứng bên trong các khe nhỏ của lá mềm, thường là ở chóp lá. Ấu trùng bọ có dạng dẹt, màu vàng ngả trắng. Chúng ăn bên trong mô lá bằng cách đào hang dọc theo trục lá, và sau đó phát triển thành nhộng bên trong lá. Bọ trưởng thành có hình dạng hơi vuông vắn, có chiều dài và chiều rộng độ 3-5 mm. Chúng có màu xanh sẫm hay đen, với các gai phủ khắp thân. Cỏ dại mọc đầy, bón quá nhiều phân, mưa lớn và độ ẩm tương đối cao là điều kiện thuận lợi cho quá trình nhiễm loại bọ gai hại lúa này.\n\nTriệu chứng: Bọ trưởng thành ăn bên ngoài biểu bì lá ở mặt trên, gây ra triệu chứng đặc trưng là các dải trắng chạy song song dọc theo trục chính của lá. Trong trường hợp nhiễm nặng, ngay cả các gân lá cũng bị ảnh hưởng, dẫn đến tình trạng xuất hiện các vết trắng lớn. Bọ trưởng thành thường xuất hiện trên các lá bị tổn thương, phần lớn ở mặt trên của lá. Ấu trùng ăn các mô màu xanh giữa hai lớp biểu bì của lá, đào hang dọc theo gân lá và gây ra các mảng trắng. Chúng ta có thể được nhìn thấy được chúng khi soi lá bị nhiễm bệnh dưới ánh sáng hoặc lướt dọc ngón tay theo đường hang. Các lớp bị nhiễm bọ khô đi, khiến cánh đồng có vẻ bạc trắng. Nhìn từ xa, các cánh đồng bị nhiễm bọ nặng trông như bị cháy bạc.\n\nĐặc điểm phát sinh: Những con trưởng thành thường xuất hiện vào thời điểm sáng sớm và ẩn nấp ở phần thấp của cây lúa suốt ngày và phá hoại mạnh nhất vào buổi sáng. Con trưởng thành của sâu – bọ gai cũng sẽ ăn lá lúa, chúng ăn chủ yếu từ ngọn lá xuống phía dưới và thích ăn phần mô non hơn, do nó mới hình thành nên mềm, dễ ăn và tiêu thụ hơn. Thông thường một con cái đẻ khoảng 55 quả trứng và đẻ ở ngọn lá của cây lúa.\n\nSố lứa sâu – bọ gai sinh ra phải phụ thuộc vào điều kiện tự nhiên (nhiệt độ, thời tiết, độ ẩm) và số lượng vụ lúa nhà nông thực hiện canh tác thường gồm 6 lứa như sau: có 1 lứa vào tháng 2 trong vụ lúa xuân, 1 lứa vào tháng 4- 5 trên cỏ, 1 lứa trên lúa cạn và 3 lứa còn lại phát sinh trên lúa mùa từ cỡ tháng 7-10. Các con trưởng thành bắt đầu xuất hiện từ tháng 2 và tăng dần số lượng quần thể cho đến tháng 6 – 7 cùng với lúc sâu non gây hại nặng trên lúa non. Nhưng sau một thời gian mật độ sâu non và trưởng thành sẽ thay đổi, chúng bắt đầu giảm sau tháng 8.\n\nSâu – bọ gai phân bố ở khắp các vùng trồng lúa trong nước, đặc biệt là ở những vùng trồng lúa năng suất cao, do đây cũng có chất lượng dinh dưỡng nhiều nhất.\n\nBiện pháp phòng ngừa:\n- Không có giống lúa đề kháng hiệu quả đối với loài bọ này.\n- Áp dụng khoảng cách cấy mạ hẹp hơn với mật độ lá phủ dày hơn có thể chịu đựng được số lượng bọ nhiều hơn.\n- Trồng sớm trong vụ mùa để tránh đỉnh điểm phát triển số lượng quần thể của bọ.\n- Cắt đỉnh chồi để ngăn bọ đẻ trứng.\n- Thu thập bọ trưởng thành bằng vợt lưới vào lúc sáng sớm khi bọ ít di chuyển.\n- Loại bỏ bất cứ loài cỏ dại nào ra khỏi cánh đồng chưa canh tác.\n- Các lá và chồi đã bị nhiễm bọ cần được cắt và đốt bỏ, hay chôn bọ dưới bùn.\n- Tránh bón phân đạm quá nhiều ở những cánh đồng bị nhiễm bọ.\n- Áp dụng luân canh để phá vỡ vòng đời của loài bọ bệnh này.";
    public static String healthyDes = "Cây lúa khoẻ mạnh";
}
[Serializable]
public class Classes
{
    public List<ReturnedClass> classes;

    float _brownConf { get; set; }
    float _healthyConf { get; set; }
    float _hispaConf { get; set; }
    float _blastConf { get; set; }
    //float _brownConf { get { return float.Parse(brownConf); } }
    //float _healthyConf { get { return float.Parse(healthyConf); } }
    //float _hispaConf { get { return float.Parse(hispaConf); } }
    //float _blastConf { get { return float.Parse(blastConf); } }

    public void Init()
    {
        //_brownConf = classes[0].confidence;
        //_healthyConf = classes[1].confidence;
        //_hispaConf = classes[2].confidence;
        //_blastConf = classes[3].confidence;
    }

    public int GetMaximumConf()
    {
        Init();
        float holder = 0.0f;
        int _class = 0;
        if (_brownConf > holder)
        {
            holder = _brownConf;
            _class = 1;
        }
        if (_healthyConf > holder)
        {
            holder = _healthyConf;
            _class = 2;
        }
        if (_hispaConf > holder)
        {
            holder = _hispaConf;
            _class = 3;
        }
        if (_blastConf > holder)
        {
            holder = _blastConf;
            _class = 4;
        }
        return _class;
    }
}
