using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using DG.Tweening;


namespace M2MQTT{
    public class MQTTManager : MonoBehaviour
    {
        [SerializeField]
        private Text temp;
        [SerializeField]
        private Text humid;

        [SerializeField]
        private CanvasGroup _canvasLayer1;
        [SerializeField]
        private CanvasGroup _canvasLayer2;
        private Tween twenFade;
        [SerializeField]
        public ToggleSwitch toggle_led;
        [SerializeField]
        public ToggleSwitch toggle_pump;

        public void Update_Status(Status_Data _status_data)
        {
            temp.text = _status_data.temperature + "°C";
            humid.text = _status_data.humidity + "%";
        }

        public void Update_Control_LED(Control_data _control_data)
        {
            if(_control_data.status == "ON"){
                toggle_led.setToggle(true);
            }
            else{
                toggle_led.setToggle(false);
            }

        }

        public void Update_Control_PUMP(Control_data _control_data)
        {
            if(_control_data.status == "ON"){
                toggle_pump.setToggle(true);
            }
            else{
                toggle_pump.setToggle(false);
            }
        }

        public Control_data Update_ControlLed_Value(Control_data _controlLed){
            _controlLed.device = "LED";
            _controlLed.status = (toggle_led.isOn ? "ON" : "OFF");
            return _controlLed;
        }

        public Control_data Update_ControlPump_Value(Control_data _controlPump){
            _controlPump.device = "PUMP";
            _controlPump.status = (toggle_pump.isOn ? "ON" : "OFF");
            return _controlPump;
        }
        public void Fade(CanvasGroup _canvas, float endValue, float duration, TweenCallback onFinish)
        {
            if (twenFade != null)
            {
                twenFade.Kill(false);
            }

            twenFade = _canvas.DOFade(endValue, duration);
            twenFade.onComplete += onFinish;
        }
        public void FadeIn(CanvasGroup _canvas, float duration)
        {
            Fade(_canvas, 1f, duration, () =>
            {
                _canvas.interactable = true;
                _canvas.blocksRaycasts = true;
            });
        }

        public void FadeOut(CanvasGroup _canvas, float duration)
        {
            Fade(_canvas, 0f, duration, () =>
            {
                _canvas.interactable = false;
                _canvas.blocksRaycasts = false;
            });
        }

        IEnumerator _IESwitchLayer()
        {
           
            FadeOut(_canvasLayer1, 0.25f);
            yield return new WaitForSeconds(0.5f);
            FadeIn(_canvasLayer2, 0.25f);
            
        
        }

          public void SwitchLayer()
        {
            StartCoroutine(_IESwitchLayer());
        }

        IEnumerator _IEReturnLayer()
        {
           
            FadeOut(_canvasLayer2, 0.25f);
            yield return new WaitForSeconds(0.5f);
            FadeIn(_canvasLayer1, 0.25f);
            
        
        }
         public void ReturnLayer()
        {
            StartCoroutine(_IEReturnLayer());
            GetComponent<M2MQTT>().exitConnect();
        }
    }

}