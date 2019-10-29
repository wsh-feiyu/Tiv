package tt.tiv.model

data class LiveZbBean(
    val zhubo: List<ZhuboBean>
)

data class ZhuboBean(
    val address: String,
    val img: String,
    val title: String
)