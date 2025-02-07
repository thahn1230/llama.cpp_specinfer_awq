# LTM: gemma-7b full precision fixed, SSM: gemma-2b full precision, 8, 6, 4, 2

./build/bin/llama-speculative -m ./mymodel/gemma-7b.gguf -md ./mymodel/gemma-2b.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 1000 -ngld 1000 -t 32 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b_gemma2-2b.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b.gguf -md ./mymodel/gemma-2b-Q8_0.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b_gemma2-2b-Q8_0.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b.gguf -md ./mymodel/gemma-2b-Q6_K.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b_gemma2-2b-Q6_K.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b.gguf -md ./mymodel/gemma-2b-Q4_K.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b_gemma2-2b-Q4_K.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b.gguf -md ./mymodel/gemma-2b-Q2_K.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b_gemma2-2b-Q2_K.txt 2>&1



# LTM: gemma-7b 8-bit fixed, SSM: gemma-2b full precision, 8, 6, 4, 2

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q8_0.gguf -md ./mymodel/gemma-2b.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q8_0_gemma2-2b.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q8_0.gguf -md ./mymodel/gemma-2b-Q8_0.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q8_0_gemma2-2b-Q8_0.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q8_0.gguf -md ./mymodel/gemma-2b-Q6_K.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q8_0_gemma2-2b-Q6_K.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q8_0.gguf -md ./mymodel/gemma-2b-Q4_K.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q8_0_gemma2-2b-Q4_K.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q8_0.gguf -md ./mymodel/gemma-2b-Q2_K.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q8_0_gemma2-2b-Q2_K.txt 2>&1

 # LTM: gemma-7b 4-bit fixed, SSM: gemma-2b full precision, 8, 6, 4, 2

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q4_K.gguf -md ./mymodel/gemma-2b.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q4_K_gemma2-2b.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q4_K.gguf -md ./mymodel/gemma-2b-Q8_0.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q4_K_gemma2-2b-Q8_0.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q4_K.gguf -md ./mymodel/gemma-2b-Q6_K.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q4_K_gemma2-2b-Q6_K.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q4_K.gguf -md ./mymodel/gemma-2b-Q4_K.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q4_K_gemma2-2b-Q4_K.txt 2>&1

./build/bin/llama-speculative -m ./mymodel/gemma-7b-Q4_K.gguf -md ./mymodel/gemma-2b-Q2_K.gguf \
 -p "// Quick-sort implementation in C (4 spaces indentation + detailed comments) and sample usage:\n\n#include" \
 -e -ngl 100 -t 4 -n 4096 -s 20 --top_k 1 --draft 16 > ./results/speculative/gemma2-7b-Q4_K_gemma2-2b-Q2_K.txt 2>&1