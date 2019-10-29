package tt.tiv.adapter

import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import tt.tiv.model.LivePtBean
import tt.tiv.model.LivePtItem
import tt.tiv.model.LiveZbBean
import tt.tiv.model.ZhuboBean
import tt.tiv.widget.LivePtItemView
import tt.tiv.widget.LiveZbItemView

/**
 * @ClassName: LivePtAdapter
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午2:35
 */
class LiveZbAdapter:RecyclerView.Adapter<LiveZbAdapter.LiveZbHolder>() {
    var list=ArrayList<ZhuboBean>()
    var listener:((itemBean:ZhuboBean)->Unit)?=null

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): LiveZbHolder {
        return LiveZbHolder(LiveZbItemView(parent.context))
    }

    override fun getItemCount(): Int {
        return list?.size
    }

    override fun onBindViewHolder(holder: LiveZbHolder, position: Int) {
        val data=list.get(position)
        val itemView=holder.itemView as LiveZbItemView
        itemView.setData(data)
        itemView.setOnClickListener {
            listener?.let {
                it(data)
            }
        }
    }

    fun updataList(result: LiveZbBean) {
        list.clear()
        list.addAll(result.zhubo)
        notifyDataSetChanged()
    }

    class LiveZbHolder(itemView: View) : RecyclerView.ViewHolder(itemView)
}