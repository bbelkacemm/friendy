<template>
    <v-dialog v-model="dialog" overlay-opacity=".1" scrollable width="85%" persistent>
        <template v-slot:activator="{ on, attrs }">
            <v-btn plain v-bind="attrs" v-on="on" v-if="add">
                <v-icon left>mdi-plus</v-icon>
                {{ $t('add') }}
            </v-btn>

            <v-btn plain v-bind="attrs" v-on="on" v-if="edit">
                <v-icon left>mdi-pencil</v-icon>
                {{ $t('edit') }}
            </v-btn>
        </template>
        <v-form v-on:submit.prevent="" ref="form">
            <v-card>
                <v-card-title class="pa-0">
                    <v-spacer></v-spacer>
                    <v-btn icon tile @click="close">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                    <v-container fluid class="pa-0">
                        <v-text-field class="mb-2" v-model="roleLabel" :rules="[validationRules.required]"
                                      outlined dense hide-details="auto"
                                      :label="$t('roleLabel').toUpperCase()"></v-text-field>
                    </v-container>
                    <v-form v-on:submit.prevent="" ref="permissionForm">
                        <v-container fluid id="permission-form" class="pa-0">
                            <v-combobox :label="$t('permissionLabel').toUpperCase()" v-model="permissionLabel"
                                        :rules="[validationRules.required]"
                                        hide-details="auto"
                                        :items="modules" outlined
                                        dense></v-combobox>
                            <v-checkbox class="pa-0 ma-0" hide-details="auto" v-model="canCreateAll"
                                        :label="capitalizeFirst($t('createAll'))"></v-checkbox>
                            <v-checkbox class="pa-0 ma-0" hide-details="auto" v-model="canCreate"
                                        :label="capitalizeFirst($t('create'))"></v-checkbox>
                            <v-checkbox class="pa-0 ma-0" hide-details="auto" v-model="canReadAll"
                                        :label="capitalizeFirst($t('readAll'))"></v-checkbox>
                            <v-checkbox class="pa-0 ma-0" hide-details="auto" v-model="canRead"
                                        :label="capitalizeFirst($t('read'))"></v-checkbox>
                            <v-checkbox class="pa-0 ma-0" hide-details="auto" v-model="canUpdateAll"
                                        :label="capitalizeFirst($t('updateAll'))"></v-checkbox>
                            <v-checkbox class="pa-0 ma-0" hide-details="auto" v-model="canUpdate"
                                        :label="capitalizeFirst($t('update'))"></v-checkbox>
                            <v-checkbox class="pa-0 ma-0" hide-details="auto" v-model="canDeleteAll"
                                        :label="capitalizeFirst($t('deleteAll'))"></v-checkbox>
                            <v-checkbox class="pa-0 ma-0" hide-details="auto" v-model="canDelete"
                                        :label="capitalizeFirst($t('delete'))"></v-checkbox>
                            <v-btn @click="addPermission" icon color="primary" tile :disabled="selectedPermissions[0]">
                                <v-icon>mdi-plus</v-icon>
                            </v-btn>
                            <v-btn @click="editPermission" icon color="green" tile :disabled="!selectedPermissions[0]">
                                <v-icon>mdi-pencil</v-icon>
                            </v-btn>
                            <v-btn @click="deletePermission" icon color="error" tile
                                   :disabled="!selectedPermissions[0]">
                                <v-icon>mdi-delete</v-icon>
                            </v-btn>
                        </v-container>
                    </v-form>
                    <v-container fluid class="pa-0 mt-2">
                        <v-data-table :headers="headers"
                                      :items="permissionsFiltered"
                                      :items-per-page="5"
                                      v-on:item-selected="onSelect($event)"
                                      v-model="selectedPermissions"
                                      show-select
                                      single-select
                                      class="elevation-0">
                            <template v-slot:item.canCreateAll="{item}">
                                <v-icon v-if="item.canCreateAll">mdi-check</v-icon>
                                <v-icon v-else>mdi-close</v-icon>
                            </template>
                            <template v-slot:item.canCreate="{item}">
                                <v-icon v-if="item.canCreate">mdi-check</v-icon>
                                <v-icon v-else>mdi-close</v-icon>
                            </template>
                            <template v-slot:item.canReadAll="{item}">
                                <v-icon v-if="item.canReadAll">mdi-check</v-icon>
                                <v-icon v-else>mdi-close</v-icon>
                            </template>
                            <template v-slot:item.canRead="{item}">
                                <v-icon v-if="item.canRead">mdi-check</v-icon>
                                <v-icon v-else>mdi-close</v-icon>
                            </template>
                            <template v-slot:item.canUpdateAll="{item}">
                                <v-icon v-if="item.canUpdateAll">mdi-check</v-icon>
                                <v-icon v-else>mdi-close</v-icon>
                            </template>
                            <template v-slot:item.canUpdate="{item}">
                                <v-icon v-if="item.canUpdate">mdi-check</v-icon>
                                <v-icon v-else>mdi-close</v-icon>
                            </template>
                            <template v-slot:item.canDeleteAll="{item}">
                                <v-icon v-if="item.canDeleteAll">mdi-check</v-icon>
                                <v-icon v-else>mdi-close</v-icon>
                            </template>
                            <template v-slot:item.canDelete="{item}">
                                <v-icon v-if="item.canDelete">mdi-check</v-icon>
                                <v-icon v-else>mdi-close</v-icon>
                            </template>
                        </v-data-table>
                    </v-container>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions class="pa-0">
                    <v-btn @click="clear" text>
                        {{ $t('clear') }}
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn @click="save" tile class="primary">
                        {{ $t('save') }}
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-form>
    </v-dialog>
</template>

<script>
import { mapActions } from 'vuex'
import { post } from '@/helpers/HTTPHelper'

export default {
    name: 'RoleForm',
    props: {
        add: Boolean,
        edit: Boolean,
        data: Object,
    },
    created: function () {
        if (this.data) {
            this.roleId = this.data.id
            this.roleLabel = this.data.label
            this.permissions = this.data.permissions.map(item => {
                item.status = 'skip'
                return item
            })
        }
    },
    data: function () {
        return {
            dialog: false,
            roleId: null,
            roleLabel: null,
            permissionId: null,
            permissionLabel: null,
            canCreateAll: false,
            canCreate: false,
            canReadAll: false,
            canRead: false,
            canUpdateAll: false,
            canUpdate: false,
            canDeleteAll: false,
            canDelete: false,
            modules: [
                'users',
                'roles',
                'permissions',
                'contexts',
                'patterns',
                'responses',
                'models',
            ],
            headers: [
                {
                    text: this.$t('permissionLabel').toUpperCase(),
                    value: 'label',
                },
                {
                    text: this.$t('createAll').toUpperCase(),
                    value: 'canCreateAll',
                },
                {
                    text: this.$t('create').toUpperCase(),
                    value: 'canCreate',
                },
                {
                    text: this.$t('readAll').toUpperCase(),
                    value: 'canReadAll',
                },
                {
                    text: this.$t('read').toUpperCase(),
                    value: 'canRead',
                },
                {
                    text: this.$t('updateAll').toUpperCase(),
                    value: 'canUpdateAll',
                },
                {
                    text: this.$t('update').toUpperCase(),
                    value: 'canUpdate',
                },
                {
                    text: this.$t('deleteAll').toUpperCase(),
                    value: 'canDeleteAll',
                },
                {
                    text: this.$t('delete').toUpperCase(),
                    value: 'canDelete',
                },
            ],
            permissions: [],
            selectedPermissions: [],
        }
    },
    computed: {
        permissionsFiltered: function () {
            return this.permissions.filter(item => item.status !== 'delete')
        },
    },
    methods: {
        clear: function () {
            this.$refs.form.clear()
        },
        save: async function () {
            if (this.$refs.form.validate()) {
                if (this.permissions.length !== 0) {
                    if (this.add) {
                        const result = await post('/roles/role', {
                            'label': this.roleLabel,
                            'permissions': this.permissions,
                        })
                        this.addRole(result.data)
                        this.dialog = false
                        this.$emit('close')
                    } else if (this.edit) {
                        const result = await post(`/roles/role/${this.roleId}`, {
                            'label': this.roleLabel,
                            'permissions': this.permissions,
                        })
                        this.editRole(result.data)
                        this.dialog = false
                        this.$emit('close')
                    }
                }
            }
        },
        addPermission: function () {
            if (this.$refs.permissionForm.validate()) {
                if (!this.permissions.find(item => item.label === this.permissionLabel)) {
                    this.permissions.push({
                        'status': 'add',
                        'label': this.permissionLabel,
                        'canCreateAll': this.canCreateAll,
                        'canCreate': this.canCreate,
                        'canReadAll': this.canReadAll,
                        'canRead': this.canRead,
                        'canUpdateAll': this.canUpdateAll,
                        'canUpdate': this.canUpdate,
                        'canDeleteAll': this.canDeleteAll,
                        'canDelete': this.canDelete,
                    })
                    this.resetPermissionForm()
                }
            }
        },
        editPermission: function () {
            if (this.$refs.permissionForm.validate()) {
                const index = this.permissions.findIndex(item => item.label === this.permissionLabel)
                this.permissions.splice(index, 1, {
                    'status': this.permissionId ? 'edit' : 'add',
                    'id': this.permissionId,
                    'label': this.permissionLabel,
                    'canCreateAll': this.canCreateAll,
                    'canCreate': this.canCreate,
                    'canReadAll': this.canReadAll,
                    'canRead': this.canRead,
                    'canUpdateAll': this.canUpdateAll,
                    'canUpdate': this.canUpdate,
                    'canDeleteAll': this.canDeleteAll,
                    'canDelete': this.canDelete,
                })
                this.resetPermissionForm()
            }
        },
        deletePermission: function () {
            const index = this.permissions.findIndex(item => item.label === this.permissionLabel)
            if (!this.permissionId) {
                this.permissions.splice(index, 1)
            } else {
                this.permissions.splice(index, 1, {
                    'status': 'delete',
                    'id': this.permissionId,
                    'label': this.permissionLabel,
                    'canCreateAll': this.canCreateAll,
                    'canCreate': this.canCreate,
                    'canReadAll': this.canReadAll,
                    'canRead': this.canRead,
                    'canUpdateAll': this.canUpdateAll,
                    'canUpdate': this.canUpdate,
                    'canDeleteAll': this.canDeleteAll,
                    'canDelete': this.canDelete,
                })
            }
            this.resetPermissionForm()
        },
        onSelect: function ({ value, item }) {
            if (value) {
                this.permissionId = item.id
                this.permissionLabel = item.label
                this.canCreateAll = item.canCreateAll
                this.canCreate = item.canCreate
                this.canReadAll = item.canReadAll
                this.canRead = item.canRead
                this.canUpdateAll = item.canUpdateAll
                this.canUpdate = item.canUpdate
                this.canDeleteAll = item.canDeleteAll
                this.canDelete = item.canDelete
            } else {
                this.resetPermissionForm()
            }
        },
        close: function () {
            this.dialog = false
            this.$emit('close')
        },
        resetPermissionForm: function () {
            this.$refs.permissionForm.reset()
            this.id = null
        },
        ...mapActions('roles', ['addRole', 'editRole']),
    },
}
</script>

<style scoped lang="sass">

#permission-form
    display: grid
    align-items: center
    justify-content: center
    grid-gap: 10px
    grid-template-columns: 1fr repeat(11, auto)

</style>
