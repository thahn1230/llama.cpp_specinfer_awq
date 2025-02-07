import subprocess
import re
import json
import time
from statistics import mean
from itertools import product
import os
from typing import Dict, Optional

# llama-speculative 명령의 고정된 부분 (옵션 제외)
BASE_LLAMA_COMMAND = [
    './build/bin/llama-speculative',
    '-e',
    '-mg', '0,1,2,3,4,5,6,7',
    '-ngl', '1000',
    '-ngld', '1000',
    '-t', '32',
    '-n', '4096',
    '-s', '20',
    '--top_k', '1',
    '--draft', '16'
]

# 모델 조합 리스트
M_MODELS = [
    './mymodel/gemma-7b.gguf',
    './mymodel/gemma-7b-Q8_0.gguf',
    './mymodel/gemma-7b-Q4_K.gguf'
]

MD_MODELS = [
    './mymodel/gemma-2b.gguf',
    './mymodel/gemma-2b-Q8_0.gguf',
    './mymodel/gemma-2b-Q6_K.gguf',
    './mymodel/gemma-2b-Q4_K.gguf',
    './mymodel/gemma-2b-Q2_K.gguf'
]

# 추출할 키 목록
METRIC_KEYS = ['n_draft', 'n_predict', 'n_drafted', 'n_accept', 'accept']

# 결과를 저장할 디렉토리
OUTPUT_DIR = './results/speculative100'

# 디렉토리가 없으면 생성
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_prompts():
    """100개의 다양한 일반 주제의 프롬프트를 생성하여 리스트로 반환"""
    prompts = [
        "Describe the process of photosynthesis and its importance to life on Earth.\n\n",
        "Explain the significance of the Renaissance period in European history.\n\n",
        "What are the main causes and effects of climate change?\n\n",
        "Discuss the impact of social media on modern society.\n\n",
        "Describe the key principles of effective time management.\n\n",
        "Explain the theory of relativity in simple terms.\n\n",
        "What are the benefits and drawbacks of renewable energy sources?\n\n",
        "Discuss the role of artificial intelligence in healthcare.\n\n",
        "Explain the concept of blockchain and its applications beyond cryptocurrency.\n\n",
        "Describe the cultural significance of traditional festivals in your country.\n\n",
        "What are the psychological effects of prolonged isolation on individuals?\n\n",
        "Explain the importance of biodiversity in maintaining ecological balance.\n\n",
        "Discuss the ethical implications of genetic engineering.\n\n",
        "Describe the evolution of human communication from ancient times to the digital age.\n\n",
        "What are the key factors contributing to economic inequality?\n\n",
        "Explain the role of government in regulating the economy.\n\n",
        "Discuss the impact of globalization on local cultures and economies.\n\n",
        "Describe the main challenges facing the education system today.\n\n",
        "What are the benefits of mindfulness and meditation practices?\n\n",
        "Explain the significance of space exploration for humanity's future.\n\n",
        "Discuss the role of literature in shaping societal values and norms.\n\n",
        "Describe the process and importance of urban planning in modern cities.\n\n",
        "What are the main causes of deforestation and how can it be prevented?\n\n",
        "Explain the concept of sustainable development and its goals.\n\n",
        "Discuss the impact of technology on the job market and employment trends.\n\n",
        "Describe the key elements of a healthy lifestyle and how to maintain them.\n\n",
        "What are the advantages and disadvantages of remote work?\n\n",
        "Explain the importance of mental health awareness in society.\n\n",
        "Discuss the role of the arts in personal and community development.\n\n",
        "Describe the significance of cultural heritage preservation.\n\n",
        "What are the main challenges in achieving global peace and security?\n\n",
        "Explain the impact of diet and nutrition on overall health.\n\n",
        "Discuss the role of sports in promoting teamwork and discipline.\n\n",
        "Describe the effects of pollution on the environment and human health.\n\n",
        "What are the benefits of learning a second language?\n\n",
        "Explain the concept of digital literacy and its importance in the modern world.\n\n",
        "Discuss the role of leadership in organizational success.\n\n",
        "Describe the main factors that influence human behavior.\n\n",
        "What are the benefits and challenges of multiculturalism in society?\n\n",
        "Explain the importance of financial literacy for individuals.\n\n",
        "Discuss the impact of tourism on local economies and cultures.\n\n",
        "Describe the process of democratic governance and its key features.\n\n",
        "What are the main causes and consequences of unemployment?\n\n",
        "Explain the role of non-governmental organizations (NGOs) in humanitarian efforts.\n\n",
        "Discuss the importance of critical thinking skills in education and everyday life.\n\n",
        "Describe the impact of media censorship on freedom of expression.\n\n",
        "What are the benefits of community service and volunteerism?\n\n",
        "Explain the concept of intellectual property and its importance in innovation.\n\n",
        "Discuss the role of renewable resources in combating environmental degradation.\n\n",
        "Describe the main components of a balanced diet.\n\n",
        "What are the advantages and disadvantages of nuclear energy?\n\n",
        "Explain the importance of emotional intelligence in personal and professional relationships.\n\n",
        "Discuss the impact of automation on various industries.\n\n",
        "Describe the key elements of effective communication.\n\n",
        "What are the main challenges in addressing homelessness?\n\n",
        "Explain the concept of globalization and its effects on international trade.\n\n",
        "Discuss the role of education in promoting social mobility.\n\n",
        "Describe the importance of water conservation and sustainable usage.\n\n",
        "What are the benefits of practicing yoga and regular physical exercise?\n\n",
        "Explain the impact of digital transformation on traditional businesses.\n\n",
        "Discuss the role of innovation in economic growth and development.\n\n",
        "Describe the main features of a democratic society.\n\n",
        "What are the benefits and drawbacks of social welfare programs?\n\n",
        "Explain the significance of renewable energy in reducing carbon emissions.\n\n",
        "Discuss the impact of cultural diversity on workplace dynamics.\n\n",
        "Describe the process of scientific research and its importance in advancing knowledge.\n\n",
        "What are the main challenges in achieving gender equality?\n\n",
        "Explain the role of public transportation in urban sustainability.\n\n",
        "Discuss the importance of ethical consumerism in modern markets.\n\n",
        "Describe the effects of noise pollution on human health and well-being.\n\n",
        "What are the benefits of lifelong learning and continuous education?\n\n",
        "Explain the concept of circular economy and its benefits.\n\n",
        "Discuss the role of technology in enhancing educational methodologies.\n\n",
        "Describe the impact of climate change on global agriculture.\n\n",
        "What are the advantages and disadvantages of nuclear power plants?\n\n",
        "Explain the importance of preserving endangered species.\n\n",
        "Discuss the role of government policies in promoting economic stability.\n\n",
        "Describe the main causes of water scarcity and potential solutions.\n\n",
        "What are the benefits of participating in team sports?\n\n",
        "Explain the significance of renewable energy sources in today's world.\n\n",
        "Discuss the impact of cultural exchange programs on international relations.\n\n",
        "Describe the importance of cybersecurity in protecting personal and organizational data.\n\n",
        "What are the main challenges in implementing universal healthcare?\n\n",
        "Explain the role of arts education in fostering creativity and critical thinking.\n\n",
        "Discuss the impact of fast fashion on the environment and society.\n\n",
        "Describe the benefits of adopting a minimalist lifestyle.\n\n",
        "What are the advantages and disadvantages of electric vehicles?\n\n",
        "Explain the importance of financial planning for future security.\n\n",
        "Discuss the role of sports in promoting physical and mental health.\n\n",
        "Describe the main factors contributing to mental health issues in adolescents.\n\n",
        "What are the benefits of implementing green building practices?\n\n",
        "Explain the concept of smart cities and their potential benefits.\n\n",
        "Discuss the impact of misinformation on public opinion and decision-making.\n\n",
        "Describe the importance of fostering innovation in the technology sector.\n\n",
        "What are the main challenges in achieving sustainable urban development?\n\n",
        "Explain the role of international organizations in addressing global issues.\n\n",
        "Discuss the benefits of cultural heritage tourism for local communities.\n\n",
        "Describe the effects of excessive screen time on children's development.\n\n",
        "What are the advantages and disadvantages of remote learning?\n\n",
        "Explain the importance of disaster preparedness and response planning.\n\n"
    ]
    return prompts

# def sanitize_filename(name):
#     """파일 이름에 사용할 수 있도록 문자열을 정리"""
#     # 경로 구분자 및 확장자를 제거하고, 기타 특수 문자를 언더스코어로 대체
#     return re.sub(r'[\/\\:.]+', '_', name)

# def run_llama(command):
#     """llama-speculative 명령을 실행하고 출력을 반환"""
#     try:
#         result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)
#         return result.stdout
#     except subprocess.TimeoutExpired:
#         print(f"Timeout expired for command: {' '.join(command)}")
#         return ""

def sanitize_filename(name: str) -> str:
    """파일 이름에 사용할 수 있도록 문자열을 정리"""
    # 경로 구분자 및 확장자를 제거하고, 기타 특수 문자를 언더스코어로 대체
    return re.sub(r'[\/\\:.]+', '_', name)

def run_llama(command: list) -> str:
    """llama-speculative 명령을 실행하고 출력을 반환"""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)
        # print(f"Command Output:\n{result.stdout}")  # 표준 출력 확인
        # print(f"Command Error Output:\n{result.stderr}")  # 표준 에러 확인
        combined_output = result.stdout + '\n' + result.stderr
        return combined_output
    except subprocess.TimeoutExpired:
        # print(f"Timeout expired for command: {' '.join(command)}")
        return ""


# def parse_metrics(output):
#     """출력에서 메트릭을 추출하여 딕셔너리로 반환"""
#     metrics = {}
#     # n_draft, n_predict, n_drafted, n_accept, accept 추출
#     match = re.search(
#         r'n_draft\s*=\s*([0-9.]+)\s*'
#         r'n_predict\s*=\s*([0-9.]+)\s*'
#         r'n_drafted\s*=\s*([0-9.]+)\s*'
#         r'n_accept\s*=\s*([0-9.]+)\s*'
#         r'accept\s*=\s*([0-9.]+)%', output
#     )
#     if match:
#         metrics['n_draft'] = float(match.group(1))
#         metrics['n_predict'] = float(match.group(2))
#         metrics['n_drafted'] = float(match.group(3))
#         metrics['n_accept'] = float(match.group(4))
#         metrics['accept'] = float(match.group(5))
#     else:
#         # 매칭되지 않으면 None으로 설정
#         for key in METRIC_KEYS:
#             metrics[key] = None
#     return metrics

def parse_metrics(output: str) -> Dict[str, Optional[float]]:
    """출력에서 메트릭을 추출하여 딕셔너리로 반환"""
    metrics: Dict[str, Optional[float]] = {key: None for key in METRIC_KEYS}
    
    # 출력의 각 라인을 개별적으로 처리
    for line in output.splitlines():
        line = line.strip()
        for key in METRIC_KEYS:
            # 'accept'는 '%'가 뒤에 붙으므로 다르게 처리
            if key == 'accept':
                pattern = rf'{key}\s*=\s*([0-9.]+)%'
            else:
                pattern = rf'{key}\s*=\s*([0-9.]+)'
            match = re.match(pattern, line)
            if match:
                try:
                    metrics[key] = float(match.group(1))
                except ValueError:
                    metrics[key] = None
    # print(f"Extracted Metrics: {metrics}")  # 추출된 메트릭 확인
    return metrics



def main():
    prompts = generate_prompts()
    
    # 모든 모델 조합 생성 (cartesian product)
    model_combinations = list(product(M_MODELS, MD_MODELS))
    total_combinations = len(model_combinations)
    
    for combo_idx, (m_model, md_model) in enumerate(model_combinations, 1):
        print(f"\n=== Processing Model Combination {combo_idx}/{total_combinations} ===")
        print(f"-m: {m_model}")
        print(f"-md: {md_model}\n")
        
        combo_results = []
        accept_values = []
        
        for idx, prompt in enumerate(prompts, 1):
            print(f"Processing prompt {idx}/{len(prompts)} for combination {combo_idx}")
            # 전체 명령 구성
            cmd = BASE_LLAMA_COMMAND + ['-m', m_model, '-md', md_model, '-p', prompt]
            output = run_llama(cmd)
            metrics = parse_metrics(output)
            run_result = {
                'model_m': m_model,
                'model_md': md_model,
                'prompt': prompt.strip(),
                'metrics': metrics,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            combo_results.append(run_result)
            if metrics['accept'] is not None:
                accept_values.append(metrics['accept'])
            # 각 실행 사이에 약간의 지연을 둘 수 있음
            time.sleep(1)  # 1초 지연
                
        # accept 값의 평균 계산
        if accept_values:
            average_accept = mean(accept_values)
        else:
            average_accept = None
        
        # JSON 파일 이름 생성
        m_model_name = sanitize_filename(os.path.basename(m_model))
        md_model_name = sanitize_filename(os.path.basename(md_model))
        json_filename = f"llama_metrics_{m_model_name}_md_{md_model_name}.json"
        json_filepath = os.path.join(OUTPUT_DIR, json_filename)
        
        # 각 모델 조합의 결과와 평균을 저장
        combination_result = {
            'model_m': m_model,
            'model_md': md_model,
            'runs': combo_results,
            'average_accept': average_accept
        }
        
        # JSON 파일로 저장
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(combination_result, f, ensure_ascii=False, indent=4)
        print(f"Completed Model Combination {combo_idx}/{total_combinations} - Average accept: {average_accept}")
        print(f"Metrics saved to {json_filepath}\n")
    
    print("All model combinations have been processed and their metrics saved.")

# def main():
#     prompts = generate_prompts()
    
#     # 모든 모델 조합 생성 (cartesian product)
#     model_combinations = list(product(M_MODELS, MD_MODELS))
#     total_combinations = len(model_combinations)
    
#     for combo_idx, (m_model, md_model) in enumerate(model_combinations, 1):
#         print(f"\n=== Processing Model Combination {combo_idx}/{total_combinations} ===")
#         print(f"-m: {m_model}")
#         print(f"-md: {md_model}\n")
        
#         combo_results = []
#         accept_values = []
        
#         for idx, prompt in enumerate(prompts, 1):
#             print(f"Processing prompt {idx}/{len(prompts)} for combination {combo_idx}")
#             # 전체 명령 구성
#             cmd = BASE_LLAMA_COMMAND + ['-m', m_model, '-md', md_model, '-p', prompt]
#             output = run_llama(cmd)
#             metrics = parse_metrics(output)
#             run_result = {
#                 'model_m': m_model,
#                 'model_md': md_model,
#                 'prompt': prompt.strip(),
#                 'metrics': metrics,
#                 'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
#             }
#             combo_results.append(run_result)
#             if metrics['accept'] is not None:
#                 accept_values.append(metrics['accept'])
#             # 각 실행 사이에 약간의 지연을 둘 수 있음
#             time.sleep(1)  # 1초 지연
                
#         # accept 값의 평균 계산
#         if accept_values:
#             average_accept = mean(accept_values)
#         else:
#             average_accept = None
        
#         # JSON 파일 이름 생성
#         m_model_name = sanitize_filename(os.path.basename(m_model))
#         md_model_name = sanitize_filename(os.path.basename(md_model))
#         json_filename = f"llama_metrics_{m_model_name}_md_{md_model_name}.json"
#         json_filepath = os.path.join(OUTPUT_DIR, json_filename)
        
#         # 각 모델 조합의 결과와 평균을 저장
#         combination_result = {
#             'model_m': m_model,
#             'model_md': md_model,
#             'runs': combo_results,
#             'average_accept': average_accept
#         }
        
#         # JSON 파일로 저장
#         with open(json_filepath, 'w', encoding='utf-8') as f:
#             json.dump(combination_result, f, ensure_ascii=False, indent=4)
#         print(f"Completed Model Combination {combo_idx}/{total_combinations} - Average accept: {average_accept}")
#         print(f"Metrics saved to {json_filepath}\n")
    
#     print("All model combinations have been processed and their metrics saved.")

if __name__ == "__main__":
    main()
