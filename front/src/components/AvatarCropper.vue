<template>
  <div class="avatar-cropper">
    <div v-if="dataUrl" class="avatar-cropper-overlay">
      <div class="avatar-cropper-mark"><a href="javascript:;" class="avatar-cropper-close" @click="destroy">&times;</a></div>
      <div class="avatar-cropper-container">
        <div class="avatar-cropper-image-container">
          <img ref="img" :src="dataUrl" alt="" @load.stop="createCropper" />
        </div>
        <div class="avatar-cropper-footer">
          <button class="avatar-cropper-btn" type="button" @click="destroy" v-text="labels.cancel">Cancel</button>
          <button class="avatar-cropper-btn" type="button" @click="submit" v-text="labels.submit">Submit</button>
        </div>
      </div>
    </div>
    <input ref="input" type="file" class="avatar-cropper-img-input" :accept="mimes">
  </div>
</template>

<script>
  import 'cropperjs/dist/cropper.css'
  import Cropper from 'cropperjs'

  export default {
    props: {
      trigger: {
        type: [String, Element],
        required: true
      },
      uploadHandler: {
        type: Function,
      },
      uploadUrl: {
        type: String,
      },
      uploadHeaders: {
        type: Object,
      },
      uploadFormName: {
        type: String,
        default: 'file'
      },
      uploadFormData: {
        type: Object,
        default() {
          return {}
        }
      },
      cropperOptions: {
        type: Object,
        default() {
          return {
            aspectRatio: 1,
            autoCropArea: 1,
            viewMode: 1,
            movable: false,
            zoomable: false,
          }
        }
      },
      outputOptions: {
        type: Object,
        default() {
          return {
            width: 512,
            height: 512
          }
        }
      },
      outputMime: {
        type: String,
        default: 'image/jpeg'
      },
      outputQuality: {
        type: Number,
        default: 0.9
      },
      mimes: {
        type: String,
        default: 'image/png, image/gif, image/jpeg, image/bmp, image/x-icon'
      },
      labels: {
        type: Object,
        default() {
          return {
            submit: "提交",
            cancel: "取消"
          }
        }
      }
    },
    data() {
      return {
        cropper: undefined,
        dataUrl: undefined,
        filename: undefined
      }
    },
    methods: {
      destroy() {
        this.cropper.destroy()
        this.$refs.input.value = '';
        this.dataUrl = undefined
      },
      submit() {
        this.$emit('submit')
        if (this.uploadUrl) {
          this.uploadImage()
        } else if (this.uploadHandler) {
          this.uploadHandler(this.cropper)
        } else {
          this.$emit('error', 'No upload handler found.', 'user')
        }
        this.destroy()
      },
      pickImage() {
        this.$refs.input.click()
      },
      createCropper() {
        this.cropper = new Cropper(this.$refs.img, this.cropperOptions)
      },
      uploadImage() {
        this.cropper.getCroppedCanvas(this.outputOptions).toBlob((blob) => {
          let form = new FormData()
          let xhr = new XMLHttpRequest()
          let data = Object.assign({}, this.uploadFormData)

          for (let key in data) {
            form.append(key, data[key])
          }

          form.append(this.uploadFormName, blob, this.filename)

          this.$emit('uploading', form, xhr)

          xhr.open('POST', this.uploadUrl, true)

          for (let header in this.uploadHeaders) {
            xhr.setRequestHeader(header, this.uploadHeaders[header])
          }

          xhr.onreadystatechange = () => {
            if (xhr.readyState === 4) {
              let response = ''
              try {
                response = JSON.parse(xhr.responseText)
              } catch (err) {
                response = xhr.responseText
              }
              this.$emit('completed', response, form, xhr)

              if ([200, 201, 204].indexOf(xhr.status) > -1) {
                this.$emit('uploaded', response, form, xhr)
              } else {
                this.$emit('error', 'Image upload fail.', 'upload', xhr)
              }
            }
          }
          xhr.send(form);
        }, this.outputMime, this.outputQuality)
      }
    },
    mounted() {
      // listen for click event on trigger
      let trigger = typeof this.trigger == 'object' ? this.trigger : document.querySelector(this.trigger)
      if (!trigger) {
        this.$emit('error', 'No avatar make trigger found.', 'user')
      } else {
        trigger.addEventListener('click', this.pickImage)
      }

      // listen for input file changes
      let fileInput = this.$refs.input
      fileInput.addEventListener('change', () => {
        if (fileInput.files != null && fileInput.files[0] != null) {
          let reader = new FileReader()
          reader.onload = (e) => {
            this.dataUrl = e.target.result
          }

          reader.readAsDataURL(fileInput.files[0])

          this.filename = fileInput.files[0].name || 'unknown'
          this.$emit('changed', fileInput.files[0], reader)
        }
      })
    }
  }
</script>

<style lang="scss">
  .avatar-cropper {
    .avatar-cropper-overlay {
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
      position: fixed;
      top:0;
      left:0;
      right:0;
      bottom:0;
      z-index: 99999;
    }

    .avatar-cropper-img-input {
      display: none;
    }

    .avatar-cropper-close {
      float: right;
      padding: 20px;
      font-size: 3rem;
      color: #fff;
      font-weight: 100;
      text-shadow: 0px 1px rgba(40, 40, 40,.3);
    }

    .avatar-cropper-mark {
      position: fixed;
      top:0;
      left:0;
      right:0;
      bottom:0;
      background: rgba(0, 0, 0, .10);
    }

    .avatar-cropper-container {
      background: #fff;
      z-index: 999;
      box-shadow: 1px 1px 5px rgba(100, 100, 100, .14);

      .avatar-cropper-image-container {
        position: relative;
        max-width: 400px;
        height: 300px;
      }
      img {
        max-width: 100%;
        height: 100%;
      }

      .avatar-cropper-footer {
        display: flex;
        align-items: stretch;
        align-content: stretch;
        justify-content: space-between;

        .avatar-cropper-btn {
          width: 50%;
          padding: 15px 0;
          cursor: pointer;
          border: none;
          background: transparent;
          outline: none;
          &:hover {
            background-color: #2aabd2;
            color: #fff;
          }
        }
      }
    }
  }
</style>
