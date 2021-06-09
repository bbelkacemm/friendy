import axios from 'axios'

const ADDRESS = 'http://localhost:5000'

export async function post(path, data, config) {
    const url = `${ADDRESS}${path}`
    try {
        const response = await axios.post(url, data, config)
        if (response.status === 201) {
            return response.data
        } else if (response.status === 200) {
            return response.data
        }
    } catch (error) {
        return error.response.data
    }
}


export async function get(path, data) {
    const url = `${ADDRESS}${path}`
    try {
        const response = await axios.get(url, {
            params: data,
        })
        if (response.status === 200) {
            return response.data
        }
    } catch (error) {
        return error.response.data
    }
}

export async function remove(path) {
    const url = `${ADDRESS}${path}`
    try {
        const response = await axios.delete(url)
        if (response.status === 200) {
            return {
                value: true,
            }
        }
    } catch (error) {
        return {
            value: false,
            message: error.response.data,
        }
    }
}
