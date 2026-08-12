// 闲鱼搜索结果去广告：只保留 item_type == "goods" 的真实商品
// 结构变化时原样放行，避免脚本抛异常导致请求挂到 timeout
try {
  const body = JSON.parse($response.body);
  const list = body?.data?.resultList;
  if (!Array.isArray(list)) {
    $done({});
  } else {
    body.data.resultList = list.filter(
      (i) => i?.data?.item?.main?.clickParam?.args?.item_type === "goods"
    );
    console.log(`闲鱼搜索去广告：${list.length} -> ${body.data.resultList.length}`);
    $done({ body: JSON.stringify(body) });
  }
} catch (e) {
  console.log(`闲鱼搜索去广告失败，已放行：${e}`);
  $done({});
}
