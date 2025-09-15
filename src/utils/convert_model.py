import onnx
import tensorflow as tf
import tf2onnx


MODEL_INPUT = "models/whirr-1-1.2b.keras"
MODEL_OUTPUT = "models/whirr-1-1.2b.onnx"


def convert_model() -> onnx.ModelProto:
    original_model = tf.keras.models.load_model(MODEL_INPUT)
    input_specs = get_layers(original_model)
    converted_model, _ = tf2onnx.convert.from_keras(
        original_model, input_signature=input_specs
    )
    return converted_model


def get_layers(original_model: tf.keras.Model) -> list[tf.TensorSpec]:
    input_specs = []
    for input_tensor in original_model.inputs:
        input_shape = input_tensor.shape[1:]
        input_spec = tf.TensorSpec(
            (None, *input_shape), tf.float32, name=input_tensor.name
        )
        input_specs.append(input_spec)
    return input_specs


def save_model(converted_model: onnx.ModelProto) -> None:
    with open(MODEL_OUTPUT, "wb") as file:
        file.write(converted_model.SerializeToString())


def verify_conversion() -> None:
    onnx_model = onnx.load(MODEL_OUTPUT)
    onnx.checker.check_model(onnx_model)


def main() -> None:
    converted_model = convert_model()
    save_model(converted_model)
    verify_conversion()


if __name__ == "__main__":
    main()
