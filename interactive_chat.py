from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# GPU 사용 가능 여부 확인
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"사용 중인 디바이스: {device}")
if torch.cuda.is_available():
    print(f"GPU 정보: {torch.cuda.get_device_name(0)}")
    print(f"GPU 메모리: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
else:
    print("CUDA를 사용할 수 없습니다. CPU를 사용합니다.")

# EXAONE 모델 로딩
model_name = "LGAI-EXAONE/EXAONE-4.0-1.2B"
print(f"모델 로딩 중: {model_name}")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16 if device.type == "cuda" else torch.float32,
    device_map="auto" if device.type == "cuda" else None
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
print("모델 로딩 완료!")

def generate_response(user_input, max_new_tokens=256, temperature=0.7, do_sample=True):
    """
    사용자 입력에 대해 EXAONE 모델의 응답을 생성합니다.
    """
    messages = [
        {"role": "user", "content": user_input}
    ]
    
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    )
    
    # GPU로 텐서 이동
    input_ids = input_ids.to(model.device)
    
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=do_sample,
            top_k=50,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # 입력 부분 제거하고 새로 생성된 텍스트만 반환
    response = tokenizer.decode(output[0][len(input_ids[0]):], skip_special_tokens=True)
    return response.strip()

def main():
    """
    대화형 인터페이스 메인 함수
    """
    print("\n=== EXAONE 4.0 대화형 인터페이스 ===")
    print("한국어, 영어, 스페인어 등 다양한 언어로 대화할 수 있습니다.")
    print("종료하려면 'quit', 'exit', '종료' 중 하나를 입력하세요.")
    print("=" * 60)
    
    conversation_count = 0
    
    while True:
        try:
            # 사용자 입력 받기
            user_input = input(f"\n[{conversation_count + 1}] 사용자: ").strip()
            
            # 종료 명령어 체크
            if user_input.lower() in ['quit', 'exit', '종료', 'q']:
                print("대화를 종료합니다. 안녕히 가세요!")
                break
            
            # 빈 입력 체크
            if not user_input:
                print("입력이 비어있습니다. 다시 입력해주세요.")
                continue
            
            # GPU 메모리 정보 출력 (GPU 사용 시)
            if device.type == "cuda":
                memory_used = torch.cuda.memory_allocated() / 1024**3
                memory_cached = torch.cuda.memory_reserved() / 1024**3
                print(f"GPU 메모리 사용: {memory_used:.2f} GB (캐시: {memory_cached:.2f} GB)")
            
            # 모델 응답 생성
            print("EXAONE이 응답을 생성중입니다...")
            response = generate_response(user_input)
            
            # 결과 출력
            print(f"EXAONE: {response}")
            print("-" * 60)
            
            conversation_count += 1
            
        except KeyboardInterrupt:
            print("\n\n프로그램이 중단되었습니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            print("다시 시도해주세요.")
        finally:
            # GPU 메모리 정리
            if device.type == "cuda":
                torch.cuda.empty_cache()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"프로그램 실행 중 오류가 발생했습니다: {e}")
    finally:
        # 프로그램 종료 시 GPU 메모리 완전 정리
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("GPU 메모리가 정리되었습니다.")
