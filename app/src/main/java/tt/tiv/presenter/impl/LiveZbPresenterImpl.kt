package tt.tiv.presenter.impl

import tt.tiv.model.LiveZbBean
import tt.tiv.net.ResponseHandler
import tt.tiv.net.impl.LiveZbRequest
import tt.tiv.presenter.interf.LiveZbPresenter
import tt.tiv.view.LiveZbView

class LiveZbPresenterImpl(var view:LiveZbView?):LiveZbPresenter, ResponseHandler<LiveZbBean> {
    override fun onSuccess(result: LiveZbBean) {
        view?.onLoad(result)
    }

    override fun onErr(msg: String?) {
        view?.onErr(msg)
    }

    override fun initdata(url: String) {
        LiveZbRequest(url,this).excute()
    }

    override fun detach() {
        if (view!=null) view=null
    }
}