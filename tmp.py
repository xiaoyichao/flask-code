您可以使用 Flask 的 `request` 对象来接收 POST 请求中的参数。具体来说，如果您想要接收文本类型的参数，可以使用 `request.form` 属性，该属性返回一个字典，其中包含所有 POST 请求中提交的表单数据。

以下是一个示例代码，演示如何接收 POST 请求中的文本参数：

```
from flask import Flask, request

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    text_param = request.form['text_param']
    # 在这里处理接收到的参数，比如将参数存储到数据库中等等
    return 'Parameter received: {}'.format(text_param)
```

在上面的代码中，我们定义了一个名为 `submit` 的路由，该路由接收 POST 请求，并从请求的表单数据中获取名为 `text_param` 的文本参数。然后我们可以在代码中对参数进行处理，比如将其存储到数据库中。最后，我们返回一个包含接收到的参数的消息，以便用户知道其参数是否被正确接收。

需要注意的是，如果您的 POST 请求中包含的参数不是文本类型，比如图片或文件等，那么您需要使用 `request.files` 属性来接收这些参数。