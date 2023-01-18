<template>
    <div id="input-field">
        <main-input-field-loader v-if="isLoading"></main-input-field-loader>
        <div id="input-field-header">
            <select v-model="selectedModelUrl">
                <option value='/generative-model/next-sentence'>다음 문장 추천해주기</option>
                <option value='/generative-model/title'>소제목 생성하기</option>
                <option value='/generative-model/good-advice'>좋은점 생성하기</option>
                <option value='/generative-model/regret-advice'>아쉬운점 생성하기</option>
                <option value='/summary-model/answer'>중요한 3문장 요약</option>
            </select>
        </div>

        <div id="input-field-content">
            <textarea name="" cols="30" rows="10" v-model="input"></textarea>
        </div>
        
        <div id="input-field-footer">
            <font-awesome-icon icon="fa-brands fa-github"></font-awesome-icon>
            <button v-on:click="analyzeInput">분석하기</button>
        </div>
    </div>
</template>

<script>
import MainInputFieldLoader from './MainInputFieldLoader.vue';

export default {
    data: function () {
        return {
            input: '',
            selectedModelUrl: '',
            analyzedResults: [],

            axiosInstance: this.$axios.create(),
            isLoading: false,
        }
    },
    created() {
        // 
        this.axiosInstance.interceptors.request.use(
            config => {
                this.isLoading = true;
                return config;
            },
            error => {
                this.isLoading = false;
                return Promise.reject(error);
            }
        );
        this.axiosInstance.interceptors.response.use(
            response => {
                this.isLoading = false;
                return response;
            },
            error => {
                this.isLoading = false;
                return Promise.reject(error);
            }
        );
    },
    components: {
        'main-input-field-loader': MainInputFieldLoader
    },
    methods: {
        analyzeInput: function () {
            const vm = this;
            this.axiosInstance.post('http://127.0.0.1:8000' + this.selectedModelUrl, {
                input: this.input
            })
            .then(function (response) {
                if (vm.selectedModelUrl == '/generative-model/next-sentence') {
                    vm.analyzedResults = response.data.generated_next_sentence
                } else if (vm.selectedModelUrl == '/generative-model/title') {
                    vm.analyzedResults = response.data.generated_title
                } else if (vm.selectedModelUrl == '/generative-model/good-advice') {
                    vm.analyzedResults = response.data.generated_good_advice
                } else if (vm.selectedModelUrl == '/generative-model/regret-advice') {
                    vm.analyzedResults = response.data.generated_regret_advice
                } else if (vm.selectedModelUrl == '/summary-model/answer') {
                    vm.analyzedResults = response.data.summarized_answer
                }
                console.log(vm.analyzedResults);
                vm.$EventBus.$emit('analyzedResults', vm.analyzedResults)
            })
            .catch(function (error) {
                console.log(error)
            });
        }
    }
}
</script>

<style scoped>
#input-field {
    /* Auto layout */
    display: flex;
    flex-direction: column;
    align-items: center;

    margin: 5% 10%;

    background: #FAFAFA;
    border: 2px solid #E9E9E9;
    border-radius: 5px;
}

#input-field-header {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    background: #FAFAFA;
}

#input-field-content {
    border-width: 1px 0px;
    border-style: solid;
    border-color: #E9E9E9;
    background: #FAFAFA;
    
    width: 100%;
    padding: 17.5px 25px;
}

#input-field-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    background: #FAFAFA;
}

textarea {
    background: #FAFAFA;
    border: none;
    resize: none;
    width: 100%;
}

textarea:focus {
    /* outline: none; */
}
</style>
