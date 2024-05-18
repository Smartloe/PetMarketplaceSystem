<template>
  <div class="footer">
    <el-row class="ng-promise-box" type="flex" justify="center">
      <el-col :span="12">
        <div class="ng-promise">
          <el-link class="promise-item" icon="el-icon-check" :underline="false">7天无理由退换货</el-link>
          <el-link class="promise-item" icon="el-icon-s-goods" :underline="false">满99元全场免邮</el-link>
          <el-link class="promise-item" icon="el-icon-s-check" :underline="false">100%品质保证</el-link>
        </div>
      </el-col>
    </el-row>
    <el-row class="mod_help" type="flex" justify="center">
      <el-col :span="12">
        <p>
          <el-link :underline="false">关于我们</el-link>
          <span>|</span>
          <el-link :underline="false">帮助中心</el-link>
          <span>|</span>
          <el-link :underline="false">售后服务</el-link>
          <span>|</span>
          <el-link :underline="false">宠物资讯</el-link>
          <span>|</span>
          <el-link :underline="false">关于货源</el-link>
        </p>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.footer {
  padding: 20px 0;
  background-color: #f5f5f5;
  color: #333;
  text-align: center;
}

.ng-promise-box {
  margin-bottom: 20px;
}

.promise-item {
  margin-right: 20px;
  font-size: 14px;
  color: #333;
}

.mod_help p {
  font-size: 14px;
  color: #333;
}

.mod_help el-link {
  margin-right: 10px;
}

/* 移除最后一个链接后面的分隔符 */
.mod_help p el-link:last-child {
  margin-right: 0;
}

/* 移除最后一个承诺项后面的margin-right */
.promise-item:last-child {
  margin-right: 0;
}
</style>