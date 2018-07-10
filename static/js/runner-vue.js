$().ready(function() {
    Vue.use(VueResource);
    new Vue({
        el: '#dashboard',
        data: {
            tasks: [],
            running: false,
            apiUrl: '/api/task/',
            checkInterval: 10,
            interval: {}
        },
        computed: {
            resource: function () {
                return this.$resource(this.apiUrl + '{slug}');
            },
        },
        created: function() {
            let vm = this;
            vm.$on('build_now', function(slug){
                let task = vm.tasks.find(x => x.slug == slug)
                if (task){
                    vm.tasks[vm.tasks.indexOf(task)].build_now = true
                }
            })
            vm.resource.get().then(function(response) {
                this.tasks = response.body;
            },function () {});
            vm.interval = setInterval(function () {
                vm.resource.get().then(function(response) {
                    this.tasks = response.body;
                },function () {})
            }, 1000 * vm.checkInterval);
            setTimeout(function () {
                $('[tooltip]').each(function(t, el){
                    $(el).tooltip({title: el.attributes.tooltip.value})
                })
            }, 300);
        },
        beforeDestroy: function (){
            clearInterval(this.interval)
            return true
        },
        components: {
            'run-now': {
                props: ['slug'],
                template: `
                    <div>
                        <i v-show="!task.build_now" class="fa fa-clock-o text-info" tooltip="Run now" v-on:click="run(slug)"></i>
                        <i v-show="task.build_now" class="fa fa-clock-o text-warning" tooltip="Added to queue"></i>
                    </div>
                `,
                computed: {
                    task: function(){
                        return this.$parent.tasks.find(x => x.slug == this.slug) || {}
                    }
                },
                methods: {
                    run: function(slug){
                        let vm = this;
                        vm.$parent.resource.save({slug: vm.slug.trim()}, data={action: 'build_now'}).then(function(response) {
                            if (response.body && response.body.success){
                                this.$emit('build_now', vm.slug)
                            }
                        });
                    }
                },
            },
            'runner-status': {
                props: ['slug'],
                template: `
                    <div>
                        <i v-show="!task.running && !task.pause" class="fa fa-sun-o text-info" tooltip="Wait"></i>
                        <i v-show="task.running" class="fa fa-certificate fa-spin text-success" tooltip="Running now"></i>
                        <i v-show="!task.running && task.pause" class="fa fa-certificate text-muted" tooltip="Paused"></i>
                    </div>
                `,
                computed: {
                    task: function(){
                        return this.$parent.tasks.find(x => x.slug == this.slug) || {}
                    }
                },
            },
            'task-status': {
                props: ['slug'],
                template: `
                    <div>
                        <span v-show="task.last_status != undefined" :class="(task.last_status? 'text-success': 'text-danger')">{{(task.last_status? 'Success': 'Error')}}</span>
                        <span v-show="task.last_status == undefined">-</span>
                    </div>
                `,
                computed: {
                    task: function(){
                        return this.$parent.tasks.find(x => x.slug == this.slug) || {}
                    }
                },
            }
        }
    })
});
