>>             params = line.split('(')[1].split(')')[0]
>>         else:
>>             params = 'ver código'
>>         print(f'{method_count:2d}. {method_name}({params}) - Línea {i}')
>>
>> print(f'\n📊 TOTAL: {method_count} métodos empresariales disponibles')
>> "
🔍 CATÁLOGO COMPLETO DE 74 MÉTODOS AI LEARNING SERVICE
================================================================================
 1. _initialize_enterprise_services(self) - Línea 108
 2. _ensure_enterprise_ai_tables_exist(self) - Línea 173
 3. _create_table_if_not_exists(ver código) - Línea 235
 4. _log_to_bigquery_enterprise(ver código) - Línea 260
 5. _log_to_bigquery_ai_with_auto_schema(ver código) - Línea 300
 6. analyze_sentiment_enterprise(ver código) - Línea 344
 7. _calculate_enterprise_sentiment(ver código) - Línea 413
 8. _analyze_context_multipliers(self, message_text: str) - Línea 521
 9. _calculate_confidence_score(ver código) - Línea 554
10. _extract_emotional_indicators(ver código) - Línea 570
11. _analyze_risk_factors(ver código) - Línea 607
12. _calculate_engagement_level(ver código) - Línea 638
13. _generate_enterprise_personalization_hints(ver código) - Línea 682
14. _log_sentiment_analysis_async(ver código) - Línea 751
15. _log_async() - Línea 761
16. _calculate_business_impact(self, sentiment_analysis: SentimentAnalysis) - Línea 791     
17. detect_enterprise_user_patterns(ver código) - Línea 805
18. _detect_enterprise_communication_pattern(ver código) - Línea 847
19. _detect_enterprise_content_preferences(ver código) - Línea 883
20. _detect_enterprise_expertise_level(ver código) - Línea 916
21. _detect_enterprise_value_seeking(ver código) - Línea 969
22. enhance_user_context_with_learning(ver código) - Línea 1008
23. process_enterprise_interaction(ver código) - Línea 1044
24. process_feedback_learning(ver código) - Línea 1099
25. _calculate_formality_score(self, message: str) - Línea 1130
26. _calculate_technical_score(self, message: str) - Línea 1189
27. _calculate_efficiency_score(self, message: str) - Línea 1210
28. _update_enterprise_performance_metrics(ver código) - Línea 1229
29. get_enterprise_performance_metrics(self) - Línea 1248
30. _log_patterns_async(self, user_id: str, patterns: List[UserPattern]) - Línea 1254       
31. _log_async() - Línea 1257
32. _calculate_pattern_roi(self, pattern: UserPattern) - Línea 1294
33. _analyze_enterprise_topics(self, message: str) - Línea 1320
34. _get_enterprise_user_patterns(self, user_id: str) - Línea 1339
35. _get_enterprise_sentiment_profile(self, user_id: str) - Línea 1380
36. log_interaction(self, **kwargs: Any) - Línea 1449
37. generate_smart_recommendations(self, user_id: str) - Línea 1453
38. _generate_enterprise_predictions(ver código) - Línea 1544
39. _calculate_user_business_value(ver código) - Línea 1635
40. _predict_next_user_action(ver código) - Línea 1685
41. _predict_user_satisfaction(self, sentiment: SentimentAnalysis) - Línea 1717
42. _get_enterprise_predictions(self, user_id: str) - Línea 1730
43. _generate_fallback_predictions(self, user_id: str) - Línea 1785
44. _generate_enterprise_personalization(ver código) - Línea 1806
45. _determine_communication_style_enterprise(ver código) - Línea 1886
46. _determine_content_depth(ver código) - Línea 1899
47. _determine_response_tone(ver código) - Línea 1912
48. _determine_urgency_level(ver código) - Línea 1925
49. _generate_enterprise_recommendations(ver código) - Línea 1946
50. _calculate_enterprise_value_score(self) - Línea 1977
51. _calculate_enterprise_business_metrics(ver código) - Línea 1988
52. _log_enterprise_business_metrics(self, metrics: Dict[str, Any]) - Línea 2062
53. _log_async() - Línea 2065
54. _analyze_depth_preference(self, message: str) - Línea 2107
55. _analyze_format_preference(self, message: str) - Línea 2116
56. _count_data_requests(self, message: str) - Línea 2125
57. _analyze_solution_orientation(self, message: str) - Línea 2130
58. _determine_communication_style(ver código) - Línea 2138
59. _engagement_level_to_score(self, engagement: Any) - Línea 2151
60. _analyze_question_pattern(self, message: str) - Línea 2169
61. _calculate_communication_business_impact(ver código) - Línea 2181
62. _predict_next_communication_action(self, pattern_data: Dict[str, Any]) - Línea 2192     
63. _calculate_content_business_impact(self, pattern_data: Dict[str, Any]) - Línea 2201     
64. _predict_next_content_action(self, pattern_data: Dict[str, Any]) - Línea 2208
65. _analyze_enterprise_feedback(ver código) - Línea 2215
66. _update_enterprise_learning_models(ver código) - Línea 2247
67. _extract_conversation_patterns(self, conversation_id: str) - Línea 2280
68. _generate_enterprise_feedback_insights(ver código) - Línea 2289
69. _determine_user_experience_level(self, user_id: str) - Línea 2324
70. _calculate_feedback_business_impact(ver código) - Línea 2334
71. _generate_personalization_updates(ver código) - Línea 2350
72. _suggest_model_adjustments(ver código) - Línea 2368
73. _generate_recommended_actions(ver código) - Línea 2384
74. process_invoice_upload_patterns(ver código) - Línea 2405
75. process_manual_data_patterns(ver código) - Línea 2420
76. process_consumption_update_patterns(ver código) - Línea 2434
77. generate_consumption_insights(ver código) - Línea 2448
78. enhance_tariff_comparison(ver código) - Línea 2474

📊 TOTAL: 78 métodos empresariales disponibles
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY> cd app/services && python -c "
>> import re
>>                                            
>> # Leer el archivo
>> with open('ai_learning_service.py', 'r', encoding='utf-8') as f:
>>     content = f.read()
>>
>> # Encontrar todos los métodos con regex más robusto
>> methods = []
>> lines = content.split('\n')
>>
>> for i, line in enumerate(lines, 1):        
>>     # Buscar definiciones de métodos
>>     if re.match(r'^\s+def\s+\w+\s*\(', line) and not 'def __' in line:
>>         # Extraer nombre del método        
>>         match = re.search(r'def\s+(\w+)\s*\((.*?)\)', line)
>>         if match:
>>             method_name = match.group(1)   
>>             params = match.group(2)        
>>             methods.append((method_name, params, i))
>>
>> print('🔍 CATÁLOGO COMPLETO DE MÉTODOS AI LEARNING SERVICE')
>> print('=' * 80)
>>
>> for idx, (name, params, line_num) in enumerate(methods, 1):
>>     # Truncar parámetros si son muy largos 
>>     short_params = params[:50] + '...' if len(params) > 50 else params
>>     print(f'{idx:2d}. {name}({short_params}) - Línea {line_num}')
>>
>> print(f'\n📊 TOTAL: {len(methods)} métodos empresariales disponibles')
>> "
🔍 CATÁLOGO COMPLETO DE MÉTODOS AI LEARNING SERVICE
================================================================================
 1. _initialize_enterprise_services(self) - Línea 108
 2. _ensure_enterprise_ai_tables_exist(self) - Línea 173
 3. _analyze_context_multipliers(self, message_text: str) - Línea 521
 4. _log_async() - Línea 761
 5. _calculate_business_impact(self, sentiment_analysis: SentimentAnalysis) - Línea 791     
 6. _calculate_formality_score(self, message: str) - Línea 1130
 7. _calculate_technical_score(self, message: str) - Línea 1189
 8. _calculate_efficiency_score(self, message: str) - Línea 1210
 9. get_enterprise_performance_metrics(self) - Línea 1248
10. _log_patterns_async(self, user_id: str, patterns: List[UserPattern]) - Línea 1254       
11. _log_async() - Línea 1257
12. _calculate_pattern_roi(self, pattern: UserPattern) - Línea 1294
13. _analyze_enterprise_topics(self, message: str) - Línea 1320
14. _get_enterprise_user_patterns(self, user_id: str) - Línea 1339
15. _get_enterprise_sentiment_profile(self, user_id: str) - Línea 1380
16. log_interaction(self, **kwargs: Any) - Línea 1449
17. generate_smart_recommendations(self, user_id: str) - Línea 1453
18. _predict_user_satisfaction(self, sentiment: SentimentAnalysis) - Línea 1717
19. _get_enterprise_predictions(self, user_id: str) - Línea 1730
20. _generate_fallback_predictions(self, user_id: str) - Línea 1785
21. _calculate_enterprise_value_score(self) - Línea 1977
22. _log_enterprise_business_metrics(self, metrics: Dict[str, Any]) - Línea 2062
23. _log_async() - Línea 2065
24. _analyze_depth_preference(self, message: str) - Línea 2107
25. _analyze_format_preference(self, message: str) - Línea 2116
26. _count_data_requests(self, message: str) - Línea 2125
27. _analyze_solution_orientation(self, message: str) - Línea 2130
28. _engagement_level_to_score(self, engagement: Any) - Línea 2151
29. _analyze_question_pattern(self, message: str) - Línea 2169
30. _predict_next_communication_action(self, pattern_data: Dict[str, Any]) - Línea 2192     
31. _calculate_content_business_impact(self, pattern_data: Dict[str, Any]) - Línea 2201     
32. _predict_next_content_action(self, pattern_data: Dict[str, Any]) - Línea 2208
33. _extract_conversation_patterns(self, conversation_id: str) - Línea 2280
34. _determine_user_experience_level(self, user_id: str) - Línea 2324

📊 TOTAL: 34 métodos empresariales disponibles
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services>
s> Get-Content "ai_learning_service.py" | Select-String "^\s+def\s+" | ForEach-Object { $_.LineNumber.ToString() + ": " + $_.Line.Trim() } | Select-Object -First 20
83: def __init__(self) -> None:
108: def _initialize_enterprise_services(self) -> None:
173: def _ensure_enterprise_ai_tables_exist(self) -> None:
235: def _create_table_if_not_exists(
260: def _log_to_bigquery_enterprise(
300: def _log_to_bigquery_ai_with_auto_schema(
344: def analyze_sentiment_enterprise(        
413: def _calculate_enterprise_sentiment(     
521: def _analyze_context_multipliers(self, message_text: str) -> Dict[str, float]:
554: def _calculate_confidence_score(
570: def _extract_emotional_indicators(       
607: def _analyze_risk_factors(
638: def _calculate_engagement_level(
682: def _generate_enterprise_personalization_hints(
751: def _log_sentiment_analysis_async(       
761: def _log_async() -> None:
791: def _calculate_business_impact(self, sentiment_analysis: SentimentAnalysis) -> str:    
805: def detect_enterprise_user_patterns(     
847: def _detect_enterprise_communication_pattern(
883: def _detect_enterprise_content_preferences(
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services>