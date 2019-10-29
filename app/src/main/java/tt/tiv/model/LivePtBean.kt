package tt.tiv.model

import android.os.Parcel
import android.os.Parcelable

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
):Parcelable{
    constructor(parcel: Parcel) : this(
        parcel.readString()!!,
        parcel.readString()!!,
        parcel.readString()!!,
        parcel.readString()!!
    ) {
    }

    override fun writeToParcel(parcel: Parcel, flags: Int) {
        parcel.writeString(Number)
        parcel.writeString(address)
        parcel.writeString(title)
        parcel.writeString(xinimg)
    }

    override fun describeContents(): Int {
        return 0
    }

    companion object CREATOR : Parcelable.Creator<LivePtItem> {
        override fun createFromParcel(parcel: Parcel): LivePtItem {
            return LivePtItem(parcel)
        }

        override fun newArray(size: Int): Array<LivePtItem?> {
            return arrayOfNulls(size)
        }
    }

}