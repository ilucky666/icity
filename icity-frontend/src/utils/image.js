// src/utils/image.js

// 预定义一组高质量的城市更新、建筑、规划类图片ID
// 均选取自 Unsplash 稳定图库
const IMAGE_IDS = [
    // 城市天际线与全景
    '1449824913935-59a10b8d2000', // 城市俯瞰
    '1477959858617-67f85cf4f1df', // 高密度城市
    '1480714378408-67cf0d13bc1b', // 繁华街区
    '1444723121867-7a241cacace9', // 摩天大楼
    '1477414348463-c0eb7f1359b6', // 现代建筑立面

    // 城市更新与建设
    '1519999482648-25049ddd37b1', // 规划图纸/施工
    '1503387762-592deb58ef4e',   // 建筑结构
    '1590274457723-5561a7a01b73', // 工业风改造
    '1532187863486-abf9dbad1b69', // 几何线条
    '1486325212027-8081e485255e', // 生态建筑

    // 街道与人文
    '1534430480-50ed1d11c43f',   // 街道人流
    '1497366216548-37526070297c', // 现代办公环境
    '1517245386807-bb43f82c33c4', // 创意园区/红砖
    '1518640467707-6811f4a6ab73', // 复古建筑细节
    '1545558014-8692077e9b5c',    // 城市桥梁

    // 补充高质量图
    '1464938050520-ef2270bb8ce8', // 夜景
    '1495539406979-bf61750d38ad', // 建筑对比
    '1512453979098-5745371131d1', // 抽象建筑
    '1429497419816-9ca5cfb4571a', // 现代公寓
    '1481277542478-632280bb77cb'  // 极简主义
];

/**
 * 简单的字符串哈希函数
 */
const hashCode = (str) => {
    let hash = 0;
    if (!str) return hash;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash);
};

/**
 * 根据项目名称生成或获取图片URL
 * 使用确定的哈希算法从预定义列表中选择一张图片
 * @param {string} name - 项目名称
 * @returns {string} 图片URL
 */
export const getImageUrl = (name) => {
    const safeName = name || 'urban';
    const index = hashCode(safeName) % IMAGE_IDS.length;
    const imageId = IMAGE_IDS[index];
    
    // 使用 Unsplash 的标准图片 URL 格式
    // 移除 auto=format 可能导致的某些兼容性问题，保留裁剪参数
    return `https://images.unsplash.com/photo-${imageId}?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80`;
};
