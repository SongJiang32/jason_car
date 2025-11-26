// Auto-generated. Do not edit!

// (in-package bluesea2.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class ControlRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.topic = null;
      this.func = null;
      this.flag = null;
      this.params = null;
    }
    else {
      if (initObj.hasOwnProperty('topic')) {
        this.topic = initObj.topic
      }
      else {
        this.topic = '';
      }
      if (initObj.hasOwnProperty('func')) {
        this.func = initObj.func
      }
      else {
        this.func = '';
      }
      if (initObj.hasOwnProperty('flag')) {
        this.flag = initObj.flag
      }
      else {
        this.flag = 0;
      }
      if (initObj.hasOwnProperty('params')) {
        this.params = initObj.params
      }
      else {
        this.params = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ControlRequest
    // Serialize message field [topic]
    bufferOffset = _serializer.string(obj.topic, buffer, bufferOffset);
    // Serialize message field [func]
    bufferOffset = _serializer.string(obj.func, buffer, bufferOffset);
    // Serialize message field [flag]
    bufferOffset = _serializer.int8(obj.flag, buffer, bufferOffset);
    // Serialize message field [params]
    bufferOffset = _serializer.string(obj.params, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ControlRequest
    let len;
    let data = new ControlRequest(null);
    // Deserialize message field [topic]
    data.topic = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [func]
    data.func = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [flag]
    data.flag = _deserializer.int8(buffer, bufferOffset);
    // Deserialize message field [params]
    data.params = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.topic);
    length += _getByteLength(object.func);
    length += _getByteLength(object.params);
    return length + 13;
  }

  static datatype() {
    // Returns string type for a service object
    return 'bluesea2/ControlRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '812e328e972e98d18e9abb089b71000e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string topic
    string func
    int8   flag
    string params
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ControlRequest(null);
    if (msg.topic !== undefined) {
      resolved.topic = msg.topic;
    }
    else {
      resolved.topic = ''
    }

    if (msg.func !== undefined) {
      resolved.func = msg.func;
    }
    else {
      resolved.func = ''
    }

    if (msg.flag !== undefined) {
      resolved.flag = msg.flag;
    }
    else {
      resolved.flag = 0
    }

    if (msg.params !== undefined) {
      resolved.params = msg.params;
    }
    else {
      resolved.params = ''
    }

    return resolved;
    }
};

class ControlResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.code = null;
      this.value = null;
    }
    else {
      if (initObj.hasOwnProperty('code')) {
        this.code = initObj.code
      }
      else {
        this.code = 0;
      }
      if (initObj.hasOwnProperty('value')) {
        this.value = initObj.value
      }
      else {
        this.value = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ControlResponse
    // Serialize message field [code]
    bufferOffset = _serializer.int32(obj.code, buffer, bufferOffset);
    // Serialize message field [value]
    bufferOffset = _serializer.string(obj.value, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ControlResponse
    let len;
    let data = new ControlResponse(null);
    // Deserialize message field [code]
    data.code = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [value]
    data.value = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.value);
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'bluesea2/ControlResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '2048e343f4bc3eabab899a87af89e425';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32   code
    string value
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ControlResponse(null);
    if (msg.code !== undefined) {
      resolved.code = msg.code;
    }
    else {
      resolved.code = 0
    }

    if (msg.value !== undefined) {
      resolved.value = msg.value;
    }
    else {
      resolved.value = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: ControlRequest,
  Response: ControlResponse,
  md5sum() { return '806ff7bf5db5481c099a10480669f74f'; },
  datatype() { return 'bluesea2/Control'; }
};
