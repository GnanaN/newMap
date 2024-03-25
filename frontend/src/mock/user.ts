import Mock from 'mockjs'

const user = Mock.mock({
  fixedUser: [
    {
      username: 'admin',
      password: 'admin111',
      avatar:
        ' https://tse4-mm.cn.bing.net/th/id/OIP-C.NNF59vntIv7760rOlX1zMgAAAA?w=187&h=188&c=7&r=0&o=5&cb=10&dpr=1.2&pid=1.7'
    },
    {
      username: 'user',
      password: 'user111',
      avatar:
        'https://tse1-mm.cn.bing.net/th/id/OIP-C.D34PjxR7ud-vxeTDvs5Z8gAAAA?w=135&h=150&c=7&r=0&o=5&cb=10&dpr=1.2&pid=1.7'
    }
  ]
})

export default()=>{
  Mock.mock('/api/login', 'post', (req: any) => {
    const { username, password } = JSON.parse(req.body)
    //从模拟数据中找
    const userItem = user.fixedUser.find(
      (item: any) => item.username === username && item.password === password
    )
    if (userItem) {
      return {
        code: 200,
        data: {
          username: userItem.username,
          avatar: userItem.avatar,
          token: 'admin-token',
        }
      }
    } else {
      return {
        code: 400,
        message: '用户名或密码错误'
      }
    }
  })
}

