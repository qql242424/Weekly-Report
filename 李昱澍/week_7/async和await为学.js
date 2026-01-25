//引入fs模块
const fs = require("fs");
//读取文件
function read() {
  return new Promise((resolve, reject) => {
    //读取方法，两个参数：路径、读取成败的函数
    fs.readFile("./resources/为学.md", (err, data) => {
      if (err) reject(err);
      resolve(data);
    });
  });
}
//async函数
async function main() {
  try {
    const passage = await read();
    console.log(passage.toString());
  } catch (e) {
    console.log(e);
  }
}
//调用函数
main();