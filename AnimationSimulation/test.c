#include <stdio.h>
#include <time.h>

long long example(void) {
    long long total = 0;
    int i;
    int tab[15] = {-70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70};
    for (i = 0; i < 15; ++i) {

	printf("%d", tab[i]);
            
	}
    return total;
}
long long example1(void) {
    long long total = 0;
    int i,nb = 70;
    int tab[15];
    for (i = 0; i < 15; ++i) {
	tab[i] = nb;
	nb -= 10;	
	printf("%d ", tab[i]);
            
	}
    return total;
}
int main(void) {
    clock_t start, end;
    double cpu_time_used;
    long long result;

    start = clock();

    result = example();

    end = clock();

    cpu_time_used = (double)(end - start) / CLOCKS_PER_SEC;
    printf("");	
    printf("\nexample 실행결과: %lld\n", result);
    printf("실행시간: %.6f초\n", cpu_time_used);

    return 0;
}
