import json
import re

# Python中的id
id = '168'

def extract_json_from_js(file_path):
    """从js文件中提取JSON数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 使用正则表达式提取JSON部分
        # 查找 var post = { ... }; 的模式
        pattern = r'var post = (\{.*?\});'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            json_str = match.group(1)
            # 解析JSON
            data = json.loads(json_str)
            return data
        else:
            print("未找到JSON数据")
            return None
            
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def find_matching_vods(data, target_id):
    """查找匹配的vods数据"""
    if not data or 'vods' not in data:
        print("数据中没有找到vods字段")
        return []
    
    matching_vods = []
    
    for vod in data['vods']:
        if 'id' in vod:
            # 拆分id，格式如 "212_5983"
            vod_id_parts = vod['id'].split('_')
            
            # 检查第一部分是否匹配目标id
            if vod_id_parts[0] == target_id:
                matching_vods.append(vod)
                print(f"找到匹配的vod: {vod['id']} - {vod.get('name', 'N/A')}")
    
    return matching_vods

def extract_sources(vods):
    """提取所有匹配vods的source信息"""
    sources = []
    
    for vod in vods:
        if 'source' in vod and vod['source']:
            print(f"\n=== {vod.get('name', 'N/A')} ===")
            print(f"ID: {vod.get('id', 'N/A')}")
            print(f"分辨率: {vod.get('resLabel', 'N/A')}")
            print(f"时长: {vod.get('ttl', 'N/A')}秒")
            
            for i, source in enumerate(vod['source']):
                if len(source) >= 2:
                    source_name = source[0]
                    source_url = source[1]
                    print(f"  源{i+1}: {source_name} - {source_url}")
                    sources.append({
                        'title': source_name,
                        'url': source_url
                    })
    
    return sources

def main():
    # 读取js文件
    js_file = 'js.js'
    data = extract_json_from_js(js_file)
    
    if data:
        print(f"成功读取JSON数据")
        print(f"目标ID: {id}")
        print(f"总共有 {len(data.get('vods', []))} 个vod")
        
        # 查找匹配的vods
        matching_vods = find_matching_vods(data, id)
        
        if matching_vods:
            print(f"\n找到 {len(matching_vods)} 个匹配的vod")
            
            # 提取source信息
            sources = extract_sources(matching_vods)
            
            print(f"\n总共提取到 {len(sources)} 个视频源")
            
            # 可以选择保存到文件
            with open('extracted_sources.json', 'w', encoding='utf-8') as f:
                json.dump(sources, f, ensure_ascii=False, indent=2)
            print("视频源信息已保存到 extracted_sources.json")
            
        else:
            print(f"没有找到ID为 {id} 的vod")
    else:
        print("无法读取JSON数据")

if __name__ == "__main__":
    main()