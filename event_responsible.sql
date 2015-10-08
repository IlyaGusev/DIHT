ATTACH DATABASE "old" AS old;
INSERT INTO activism_responsibleevent (id, event_id, user_id, done)
SELECT id, event_id, user_id, 0 from old.activism_event_responsible;
