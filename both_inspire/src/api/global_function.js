
function guid () {
  function S4 () {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
  }
  return (S4() + S4() + '-' + S4() + '-' + S4() + '-' + S4() + '-' + S4() + S4() + S4())
}

function test (p1, p2) {
  console.log('测试公用方法调用')
  console.log(p1 + p2)
}

export default {
// Vue.js的插件应当有一个公开方法 install。这个方法的第一个参数是 Vue 构造器，第二个参数是一个可选的选项对象。
  install: function (Vue) {
    Vue.prototype.Guid = () => guid()
    Vue.prototype.Test = (p1, p2) => test(p1, p2)
  }
}
