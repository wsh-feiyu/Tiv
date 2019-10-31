package tt.tiv.presenter.impl

import tt.tiv.model.LivePtBean
import tt.tiv.net.BaseRequest
import tt.tiv.net.ResponseHandler
import tt.tiv.net.impl.LivePtRequest
import tt.tiv.presenter.interf.LivePtPresenter
import tt.tiv.view.LivePtView

/**
 * @ClassName: LivePtPresenterImpl
 * @Description: java类作用描述
 * @Author: wsh
 * @Date: 19-10-28 下午12:19
 */
class LivePtPresenterImpl(var view:LivePtView?):LivePtPresenter, ResponseHandler<LivePtBean> {
    override fun onSuccess(result: LivePtBean) {
        view?.onLoad(result)
    }

    override fun onErr(msg: String?) {
        view?.onErr(msg)
    }


    override fun initdata(url:String) {
        LivePtRequest(url+"json.txt",this).excute()
    }


    override fun detach() {
        if (view!=null) view=null
    }
}