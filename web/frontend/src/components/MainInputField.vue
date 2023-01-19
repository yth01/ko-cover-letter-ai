<template>
    <div id="input-field" v-bind:style="{ border: inputFieldBorder }">
        <main-input-field-loader v-if="isLoading"></main-input-field-loader>
        <v-snackbar v-model="isSnackbar" :timeout="1000" :light="true" :min-width="0" color="blue" dense shoped text rounded centered>
            <v-icon color="blue" class="mr-2">mdi-check-circle</v-icon>복사되었습니다.
        </v-snackbar>
        <div id="input-field-header">
            <v-select v-model="selectedModelUrl" label="무엇을 도와드릴까요?" :items="modelList" item-text="name" item-value="value" background-color="#FAFAFA" filled rounded hide-details></v-select>
        </div>

        <div id="input-field-content">
            <textarea id="input-textfield" v-on:focus="focusInputField" v-on:blur="blurInputField" cols="20" rows="10" v-model="input"></textarea>
            
            <v-btn id="close-icon" icon elevation="0" v-on:click="clearInput" v-on:mouseover="highlightingIcon"
                v-on:mouseout="revertingIcon" v-bind:style="{ opacity: iconOpacity }">
                <v-icon>mdi-close</v-icon>
            </v-btn>
            <!-- <v-icon>mdi-close</v-icon> -->
        </div>
        <div id="input-field-footer">
            <v-btn id="copy-icon" elevation="0" v-on:click="copyInput" v-on:mouseover="highlightingIcon"
            v-on:mouseout="revertingIcon" v-bind:style="{ opacity: iconOpacity }">
                <v-icon>mdi-content-copy</v-icon>
            </v-btn>
            <v-btn id="analysis-button" v-on:click="analyzeInput" color="primary" elevation="0" tile>분석하기</v-btn>
        </div>
    </div>
</template>

<script>
import MainInputFieldLoader from './MainInputFieldLoader.vue';

export default {
    data: function () {
        return {
            input: '',
            modelList: [
                { name: '다음 문장을 생성하기', value: '/generative-model/next-sentence' },
                { name: '소제목 추천받기', value: '/generative-model/title' },
                { name: '좋은 점 조언 받기', value: '/generative-model/good-advice' },
                { name: '아쉬운 점 조언 받기', value: '/generative-model/regret-advice' },
                { name: '잘 나타나는 3문장 알아보기', value: '/summary-model/answer' }
            ],
            selectedModelUrl: '',
            analyzedResults: [],

            axiosInstance: this.$axios.create(),
            isLoading: false,
            isSnackbar: false,

            inputFieldBorder: '3px solid #E9E9E9',
            iconOpacity: 0.7,
        }
    },
    created() {
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
            vm.$EventBus.$emit('clearOutput')
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
                vm.$EventBus.$emit('analyzedResults', vm.analyzedResults)
            })
            .catch(function (error) {
                console.log(error)
            });
        },

        focusInputField: function() {
            this.inputFieldBorder = '3px solid #1976D2'
        },
        blurInputField: function() {
            this.inputFieldBorder = '3px solid #E9E9E9'
        },

        copyInput: function () {
            this.$copyText(this.input)
            .then(() => {
                this.isSnackbar = true
            })
            .catch((error) => {
                console.log(error);
            })
        },
        highlightingIcon: function () {
            this.iconOpacity = 1
        },
        revertingIcon: function () {
            this.iconOpacity = 0.7
        },
        clearInput: function() {
            this.input = ''
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

    margin: 2% 14%;

    background: #FAFAFA;
    border-radius: 10px;

    transition: border 0.2s;
}

#input-field-header {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    background: #FAFAFA;
    border-radius: 10px;
    font-family: NanumSquareNeo-dEb;
}

#input-field-content {
    display: flex;
    flex-direction: row;
    align-items: flex-start;

    border-width: 1px 0px;
    border-style: solid;
    border-color: #E9E9E9;
    background: #FAFAFA;
    
    width: 100%;
    padding: 17.5px 25px;
}

#input-textfield {
    background: #FAFAFA;
    border: none;
    resize: none;
    width: 100%;
}

#input-textfield:focus {
    outline: none;
}

#input-field-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    background: #FAFAFA;
    border-radius: 10px;
    height: 3em;
}

#copy-icon {
    border-right: 1px solid #E9E9E9;
    padding: 7.5px 15px;
    background: #FAFAFA;
    border-bottom-left-radius: 10px;
    height: 100%;
}

#analysis-button {
    border-bottom-right-radius: 5px;
    height: 100%;
}

#close-icon {
    margin-left: 25px;
}
</style>
