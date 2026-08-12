// 闲鱼首页信息流去广告：只保留 bizType == "item" 的真实商品卡
// 结构变化时原样放行，避免脚本抛异常导致请求挂到 timeout
try {
  const body = JSON.parse($response.body);
  const sections = body?.data?.sections;
  if (!Array.isArray(sections)) {
    $done({});
  } else {
    body.data.sections = sections.filter((i) => i?.data?.bizType === "item");
    body.data.feedsCount = body.data.sections.length;
    console.log(`闲鱼首页去广告：${sections.length} -> ${body.data.sections.length}`);
    $done({ body: JSON.stringify(body) });
  }
} catch (e) {
  console.log(`闲鱼首页去广告失败，已放行：${e}`);
  $done({});
}
