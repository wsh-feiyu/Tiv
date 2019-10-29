package tt.tiv.model

/**
 * @ClassName: LivePtBean
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午1:41
 */
data class LivePtBean(
    val pingtai: List<LivePtItem>
)

data class LivePtItem(
    val Number: String,
    val address: String,
    val title: String,
    val xinimg: String
)