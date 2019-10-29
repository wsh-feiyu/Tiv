package tt.tiv.adapter

import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import tt.tiv.model.LivePtBean
import tt.tiv.model.LivePtItem
import tt.tiv.widget.LivePtItemView

/**
 * @ClassName: LivePtAdapter
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午2:35
 */
class LivePtAdapter:RecyclerView.Adapter<LivePtAdapter.LivePtHodler>() {
    var list=ArrayList<LivePtItem>()

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): LivePtHodler {
        return LivePtHodler(LivePtItemView(parent.context))
    }

    override fun getItemCount(): Int {
        return list?.size
    }

    override fun onBindViewHolder(holder: LivePtHodler, position: Int) {
        val data=list.get(position)
        val itemView=holder.itemView as LivePtItemView
        itemView.setData(data)
    }

    fun updataList(result: LivePtBean) {
        list.clear()
        list.addAll(result.pingtai)
        notifyDataSetChanged()
    }

    class LivePtHodler(itemView: View) : RecyclerView.ViewHolder(itemView)
}